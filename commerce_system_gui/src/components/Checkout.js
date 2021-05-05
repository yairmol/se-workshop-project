import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Paper from '@material-ui/core/Paper';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Link from '@material-ui/core/Link';
import Typography from '@material-ui/core/Typography';
import AddressForm from './AddressForm';
import PaymentForm from './PaymentForm';
import Review from './Review';
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {useAuth} from "./use-auth";
import {useFormik} from "formik";
import {get_cart_info, purchase_cart, purchase_shopping_bag} from "../api";
import {CircularProgress} from "@material-ui/core";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

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

function getStepContent(step, formik, cart) {
  switch (step) {
    case 0:
      return <AddressForm formik={formik} />;
    case 1:
      return <PaymentForm formik={formik}/>;
    case 2:
      return <Review formik={formik} cart={cart}/>;
    default:
      throw new Error('Unknown step');
  }
}


export function Checkout() {
  const classes = useStyles();
  const {shop_id} = useParams();
  const auth = useAuth();
  const [shoppingCart, setShoppingCart] = useState({shopping_bags: []});
  const [loaded, setLoaded] = useState();
  const [activeStep, setActiveStep] = React.useState(0);

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
     onSubmit: values => {
       (shop_id ? purchase_shopping_bag(auth.getToken(), shop_id, values): purchase_cart(auth.getToken(), values))
           .then((res) => {
         alert(JSON.stringify(res));
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
      <CssBaseline />
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
                {getStepContent(activeStep, formik, shoppingCart)}
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
        <Copyright />
      </main>
    </React.Fragment> : <CircularProgress/>
  );
}
