import {useEffect, useState} from "react";
import {
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle, TableCell,
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
  {id: 'offer_maker', label: 'Offer Maker'},
  {id: 'offer', label: 'Offer'},
  {id: 'offer_state', label: 'Offer State'}
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
    auth.getToken().then((token) =>
      reply_offer(token, shopId, product.product_id, offer.offer_maker, action).then((res) => {
        if (res) {
          alert(`offer was ${action}ed successfully`);
        }
        setLoaded(false);
      })
    )
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
          </TableRow>
        </TableHead>
        <TableBody>
          {offers.map((offer) => (
            <TableRow key={offer.offer_maker}>
              {columns.map((col) =>
                <TableCell component="th" scope="row">
                  {offer[col.id]}
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
