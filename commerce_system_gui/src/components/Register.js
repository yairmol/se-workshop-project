import 'date-fns';
import React, {useState} from 'react';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from '@material-ui/pickers'
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { useFormik } from 'formik';
import {
  Link as RouteLink, useHistory,
} from 'react-router-dom';
import {useAuth} from "./use-auth";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    // width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function Register() {
  const classes = useStyles();
  const auth = useAuth();
  const [birthDate, setBirthDate] = useState(new Date());
  const history = useHistory();

  const onBirthDateChange = (date) => {
    setBirthDate(date);
  }

  const formik = useFormik({
     initialValues: {
       username: '',
       password: '',
     },
     onSubmit: values => {
       // alert(JSON.stringify(values));
       auth.signup({birthDate: birthDate, ...values}).then((res) => {
         if (res) {
           alert("registered successfully, redirecting to login");
           history.replace({ pathname: "/login", header: "Login"})
         }
       })
     },
   });

  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <form onSubmit={formik.handleSubmit} className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            type="username"
            onChange={formik.handleChange}
            value={formik.values.username}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange={formik.handleChange}
            value={formik.values.password}
          />
          <KeyboardDatePicker
          margin="normal"
          format="MM/dd/yyyy"
          id="birthDate"
          name="birthDate"
          label="Date picker inline"
          value={birthDate}
          onChange={onBirthDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
          variant="contained"
          fullWidth/>
          <Button
            type="submit"
            fullWidth
            variant="outlined"
            color="primary"
            className={classes.submit}
          >
            Register
          </Button>
        </form>
      </div>
    </Container>
    </MuiPickersUtilsProvider>
  );
}
