import React, {useEffect, useState} from 'react';
import {useAuth} from "./use-auth";
import {UserTransactions} from "./Transactions";
import Grid from "@material-ui/core/Grid";
import {Paper} from "@material-ui/core";
import {makeStyles} from "@material-ui/core/styles";
import {get_appointments, open_shop} from "../api";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import {Link as RouteLink} from "react-router-dom";
import {useFormik} from "formik";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Link from "@material-ui/core/Link";
import {Offers} from "./Offers";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    width: "auto",
  },
  form: {
    // width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
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
  heading2: {
    fontSize: theme.typography.pxToRem(20),
    flexBasis: '33.33%',
    flexShrink: 0,
    fontWeight: 530,
    padding: theme.spacing(1)
  },
  spacer: {
    margin: theme.spacing(3)
  }
}));

function UserAppointments({appointments}) {
  const classes = useStyles();

  return (<div>
      <Typography className={classes.heading2}>Appointments</Typography>
      {(appointments instanceof Array && appointments.length > 0) ?
        appointments.map((appointment) => {
          return (
            <Grid container direction="column">
              <Paper className={classes.paper}>
                <RouteLink to={{pathname: `/shops/${appointment.shop_id}`, header: appointment.shop_name}}
                           style={{color: "black"}}>
                  <Link className={classes.heading}>
                    Appointment for shop {appointment.shop_name}
                  </Link>
                </RouteLink>
                <Typography className={classes.secondaryHeading}>title: {appointment.title}</Typography>
                <Typography className={classes.secondaryHeading}>appointer: {appointment.appointer}</Typography>
              </Paper>
            </Grid>
          )
        }) : <Typography align="center">You are currently not an owner or manager of any shop</Typography>
      }
    </div>
  )
}

function OpenShopForm({openShop}) {
  const classes = useStyles();

  const formik = useFormik({
      initialValues: {
        shop_name: '',
        description: '',
        image_url: '',
      },
      onSubmit: values => openShop(values)
    }
  )

  return (
    <Grid container>
      <CssBaseline/>
      <div className={classes.paper}>
        <form onSubmit={formik.handleSubmit} className={classes.form} noValidate>
          <TextField variant="outlined" margin="normal" required fullWidth id="shop_name"
                     label="Shop Name" name="shop_name" autoFocus type="shop_name" onChange={formik.handleChange}
                     value={formik.values.shop_name}/>
          <TextField variant="outlined" margin="normal" required fullWidth id="description"
                     label="Description" name="description" autoFocus type="description" onChange={formik.handleChange}
                     value={formik.values.description}/>
          <TextField variant="outlined" margin="normal" fullWidth id="image_url"
                     label="Image url" name="image_url" autoFocus type="image_url" onChange={formik.handleChange}
                     value={formik.values.image_url}/>
          <Button type="submit" fullWidth variant="outlined" color="primary" className={classes.submit}>
            Open
          </Button>
        </form>
      </div>
    </Grid>
  );
}

export default function ProfilePage() {
  const classes = useStyles();
  const auth = useAuth();
  const [appointments, setAppointments] = useState(false)
  const [openingShop, setOpeningShop] = useState(false);

  const openShop = (shop_details) => {
    auth.getToken().then((token) => {
      open_shop(token, shop_details).then((_) => {
        setOpeningShop(false);
        setAppointments(false);
      })
    })
  }

  useEffect(() => {
    if (!appointments) {
      auth.getToken().then((token) => {
        get_appointments(token).then((res) => {
          setAppointments(res)
        })
      })
    }
  })

  return (
    <Grid container>
      <Grid item xs={12}>
        <Grid container>
          <UserTransactions/>
          <Grid item xs={5}>
            <Grid container direction="column">
              {appointments && <UserAppointments appointments={appointments}/>}
              <div className={classes.spacer}/>
              {openingShop ? <OpenShopForm openShop={openShop}/> :
                <Button color="primary" variant="outlined" onClick={() => setOpeningShop(true)}>Open Shop</Button>}
            </Grid>
          </Grid>
          <Offers />
        </Grid>
      </Grid>
    </Grid>
  );
}