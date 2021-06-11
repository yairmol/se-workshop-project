import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Link,
  Paper
} from "@material-ui/core";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import React, {useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {accept_counter_offer, delete_offer, get_user_purchase_offers} from "../api";
import Button from "@material-ui/core/Button";


const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(20),
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  info: {
    fontSize: theme.typography.pxToRem(15),

  },
  accordion: {
    flexGrow: 1
  },
  paper: {
    padding: theme.spacing(3),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  }
}));

function ProductView({product}) {
  const classes = useStyles();

  return (
    <Paper className={classes.paper}>
      <Grid container spacing={5} direction="row" alignItems="center">
        <Grid item>
          <Typography className={classes.secondaryHeading}>name: {product.product_name}</Typography>
        </Grid>
        <Grid item>
          <Typography className={classes.secondaryHeading}>original price: {product.price}</Typography>
        </Grid>
      </Grid>
    </Paper>
  )
}

function Offer({offer, index, refresh}) {
  const classes = useStyles();
  const [expanded, setExpanded] = useState(false);
  const auth = useAuth();
  const onChange = () => {
    setExpanded(!expanded)
  }

  const approve_counter = () => {
    auth.getToken().then((token) =>
      accept_counter_offer(token, offer.product.shop_id, offer.product.product_id)
        .then((res) => {
          if (res) {
            alert("successfully accepted counter offer")
          }
          refresh()
        }))
  }

  const deleteOffer = () => {
    auth.getToken().then((token) =>
      delete_offer(token, offer.product.shop_id, offer.product.product_id).then((res) => {
        if (res) {
          alert("successfully deleted offer");
        }
        refresh()
      }))
  }

  return (
    <Accordion expanded={expanded} onChange={onChange}>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon/>}
        aria-controls={`panel${index}bh-content`}
        id={`panel${index}bh-header`}
      >
        <Grid spacing={2} container direction="column">
          <Grid item>
            <Link className={classes.heading}>Offer for {offer.product.product_name}</Link>
          </Grid>
          <Grid item>
            <Typography className={classes.secondaryHeading}>offer price: {offer.offer}</Typography>
          </Grid>
          <Grid item>
            <Typography className={classes.secondaryHeading}>offer status: {offer.offer_state}</Typography>
          </Grid>
        </Grid>
      </AccordionSummary>
      <AccordionDetails>
        <Grid spacing={1} container direction="column">
          <Grid item>
            <Grid container spacing={2}>
              {offer.offer_state === "COUNTER" &&
              <Grid item>
                <Button variant="outlined" onClick={approve_counter}>
                  Accept Counter Offer
                </Button>
              </Grid>
              }
              <Grid item>
                <Button variant="outlined" onClick={deleteOffer}>
                  Delete Offer
                </Button>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Typography>Product Info</Typography>
          </Grid>
          <Grid item>
            <ProductView product={offer.product}/>
          </Grid>
        </Grid>
      </AccordionDetails>
    </Accordion>
  );
}

export function Offers() {
  const classes = useStyles();
  const [offers, setOffers] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const auth = useAuth();

  useEffect(() => {
    auth.getToken().then((token) =>
      get_user_purchase_offers(token).then((res) => {
        setOffers(res || []);
        setLoaded(true);
      }).catch((err) => setOffers([])))
  }, [loaded, auth])

  const refresh = () => {
    setLoaded(false);
  }

  return (
    <Grid item xs={6} spacing={3}>
      <Typography className={classes.heading}>Purchase Offers</Typography>
      {(offers && offers.length > 0) ?
        offers.map((offer, index) =>
          <Offer offer={offer} index={index} refresh={refresh}/>) :
        <Typography align="center">
          You currently have no purchase offers
        </Typography>
      }
    </Grid>
  );
}