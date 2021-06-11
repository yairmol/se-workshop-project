import React, {useEffect, useState} from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle, TableCell, TextField,
} from "@material-ui/core";
import Button from "@material-ui/core/Button";
import {useAuth} from "../use-auth";
import {get_offers, reply_offer} from "../../api";
import TableContainer from "@material-ui/core/TableContainer";
import Paper from "@material-ui/core/Paper";
import {makeStyles} from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";


const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const columns = [
  {id: 'offer_maker', label: 'Offer Maker', type: 'text'},
  {id: 'offer', label: 'Offer', type: 'text-field'},
  {id: 'offer_state', label: 'Offer State', type: 'text'}
]

export default function OffersPopup({shopId, product, close}) {
  const classes = useStyles();

  const auth = useAuth();
  const [offers, setOffers] = useState([]);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    if (!loaded) {
      auth.getToken().then((token) =>
        get_offers(token, shopId, product.product_id).then((res) => {
          if (res) {
            setOffers(res)
            setLoaded(true)
          }
        })
      )
    }
  })

  const reply = (offer, action) => {
    const additional_params = action === 'counter' ? {counter_offer: offer.offer} : {};
    auth.getToken().then((token) =>
      reply_offer(token, shopId, product.product_id, offer.offer_maker, action, additional_params).then((res) => {
        if (res) {
          alert(`offer was ${action}ed successfully`);
        }
        setLoaded(false);
      })
    )
  }

  const onOfferChange = (e, i) => {
    const newOffers = offers.slice(0);
    newOffers[i].offer = e.target.value;
    setOffers(newOffers);
  }

  return (
    <div>
      <Dialog
        open={true}
        onClose={close}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Manage offers for product {product.product_name}
        </DialogTitle>
        <DialogContent>
          <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            {columns.map((col) => <TableCell>{col.label}</TableCell>)}
            <TableCell>Approve</TableCell>
            <TableCell>Reject</TableCell>
            <TableCell>Counter</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {offers.map((offer, i) => (
            <TableRow key={offer.offer_maker}>
              {columns.map((col) =>
                <TableCell component="th" scope="row">
                  {col.type === 'text' ? offer[col.id] :
                    col.type === 'text-field' ?
                      <TextField id={`${offer.offer_maker}-${col.id}`} label="offer" value={offer[col.id]}
                       onChange={(e) => onOfferChange(e, i)} /> : offer[col.id]
                  }
                </TableCell>)
              }
              <TableCell>
                <Button variant="outlined" onClick={() => reply(offer, "approve")}>
                  Approve
                </Button>
              </TableCell>
              <TableCell>
                <Button variant="outlined" onClick={() => reply(offer, "reject")}>
                  Reject
                </Button>
              </TableCell>
              <TableCell>
                <Button variant="outlined" onClick={() => reply(offer, "counter")}>
                  Counter
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={close} color="primary">
            Done
          </Button>
          <Button onClick={close} color="primary" autoFocus>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
