import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Paper from '@material-ui/core/Paper';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import AddressForm from './AddressForm';
import PaymentForm from './PaymentForm';
import Review from './Review';
import {useHistory, useLocation, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {useAuth} from "./use-auth";
import {useFormik} from "formik";
import {get_cart_info, purchase_cart, purchase_shopping_bag} from "../api";
import {CircularProgress} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  appBar: {
    position: 'relative',
  },
  layout: {
    width: 'auto',
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(2) * 2)]: {
      width: 600,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(3),
    padding: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(3) * 2)]: {
      marginTop: theme.spacing(6),
      marginBottom: theme.spacing(6),
      padding: theme.spacing(3),
    },
  },
  stepper: {
    padding: theme.spacing(3, 0, 5),
  },
  buttons: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  button: {
    marginTop: theme.spacing(3),
    marginLeft: theme.spacing(1),
  },
}));

const steps = ['Shipping address', 'Payment details', 'Review your order'];

function getStepContent(step, formik, cart, cart_or_sb) {
  switch (step) {
    case 0:
      return <AddressForm formik={formik}/>;
    case 1:
      return <PaymentForm formik={formik}/>;
    case 2:
      return cart_or_sb === "cart" ? <Review formik={formik} cart={cart}/> :
        <Review formik={formik} shoppingBag={cart.shopping_bags[cart_or_sb]}/>;
    default:
      throw new Error('Unknown step');
  }
}


export function Checkout() {
  const classes = useStyles();
  const {shop_id} = useParams();
  const auth = useAuth();
  const [shoppingCart, setShoppingCart] = useState({shopping_bags: []});
  const [loaded, setLoaded] = useState(false);
  const [activeStep, setActiveStep] = React.useState(0);
  const location = useLocation();
  if (location.from === "cart"){
    localStorage.setItem("checkout", location.cart ? "cart" : location.shop_id)
  }
  const cart_or_sb = localStorage.getItem("checkout");
  const history = useHistory();
  let { from } = location.state || (auth.user ? { from: { pathname: "/transactions", header: "Transactions" } } :
    { from: { pathname: "/", header: "Main Page" } });


  useEffect(async () => {
    if (!loaded) {
      await get_cart_info(await auth.getToken()).then((res) => {
        if (res) {
          setShoppingCart(res);
        }
      })
      setLoaded(true);
      // alert(shoppingCart)
    }
  }, []);

  const payment_details = (details) => ({
    cardName: details.cardName,
    cardNumber: details.cardNumber,
    expDate: details.expDate,
    cvv: details.cvv,
  })

  const delivery_details = (details) => ({
    firstName: details.firstName,
    lastName: details.lastName,
    address1: details.address1,
    address2: details.address2,
    city: details.city,
    country: details.country,
    zip: details.zip,
  })

  const formik = useFormik({
    initialValues: {
      firstName: '',
      lastName: '',
      address1: '',
      address2: '',
      city: '',
      country: '',
      zip: '',
      cardName: '',
      cardNumber: '',
      expDate: '',
      cvv: '',
    },
    validate: values => {
      const errors = {};
      for (const key in values){
        if (!values[key]){
          errors[key] = `${key} cant be empty`;
        }
      }
      if(!/^[0-9]{16}$/i.test(values.cardNumber)){
        errors.cardNumber = "card number must be 16 digits"
      }
      if(!/^[0-9]{3}$/i.test(values.cvv)){
        errors.cvv = "cvv must be 3 digits"
      }
      if(!/^(10|11|12|0[1-9])\/[2-9][0-9]$/i.test(values.expDate)){
        errors.expDate = "expiration date must be a valid MM/YY date"
      }
      return errors;
    },
    onSubmit: values => {
      auth.getToken().then((token) => shop_id ?
        purchase_shopping_bag(token, shop_id, payment_details(values), delivery_details(values)) :
        purchase_cart(token, payment_details(values), delivery_details(values)))
        .then((res) => {
          if(res){
            alert("Purchase made successfully");
            localStorage.removeItem("checkout");
            history.replace(from);

          }
        });
    },
  });

  const handleNext = () => {
    setActiveStep(activeStep + 1);
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  return (loaded ?
      <React.Fragment>
        <CssBaseline/>
        {/*<AppBar position="absolute" color="default" className={classes.appBar}>*/}
        {/*  <Toolbar>*/}
        {/*    <Typography variant="h6" color="inherit" noWrap>*/}
        {/*      Company name*/}
        {/*    </Typography>*/}
        {/*  </Toolbar>*/}
        {/*</AppBar>*/}
        <main className={classes.layout}>
          <Paper className={classes.paper}>
            <Typography component="h1" variant="h4" align="center">
              Checkout
            </Typography>
            <Stepper activeStep={activeStep} className={classes.stepper}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
            <React.Fragment>
              {activeStep === steps.length ? (
                <React.Fragment>
                  <Typography variant="h5" gutterBottom>
                    Thank you for your order.
                  </Typography>
                  <Typography variant="subtitle1">
                    Your order number is #2001539. We have emailed your order confirmation, and will
                    send you an update when your order has shipped.
                  </Typography>
                </React.Fragment>
              ) : (
                <React.Fragment>
                  {getStepContent(activeStep, formik, shoppingCart, cart_or_sb)}
                  <div className={classes.buttons}>
                    {activeStep !== 0 && (
                      <Button onClick={handleBack} className={classes.button}>
                        Back
                      </Button>
                    )}
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={activeStep === steps.length - 1 ? formik.handleSubmit : handleNext}
                      className={classes.button}
                    >
                      {activeStep === steps.length - 1 ? 'Place order' : 'Next'}
                    </Button>
                  </div>
                </React.Fragment>
              )}
            </React.Fragment>
          </Paper>
        </main>
      </React.Fragment> : <CircularProgress/>
  );
}
