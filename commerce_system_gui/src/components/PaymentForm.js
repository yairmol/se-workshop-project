import React from 'react';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

export default function PaymentForm({formik}) {
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Payment method
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField required id="cardName" value={formik.values.cardName} onChange={formik.handleChange}
                     label="Name on card" fullWidth autoComplete="cc-name"
                     error={formik.errors.cardName} helperText={formik.errors.cardName}/>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            required
            id="cardNumber"
            label="Card number"
            fullWidth
            autoComplete="cc-number"
            value={formik.values.cardNumber}
            onChange={formik.handleChange}
            error={formik.errors.cardNumber} helperText={formik.errors.cardNumber}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField required id="expDate" value={formik.values.expDate} onChange={formik.handleChange}
                     label="Expiry date" fullWidth autoComplete="cc-exp"
                     error={formik.errors.expDate} helperText={formik.errors.expDate}/>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            required
            id="cvv"
            label="CVV"
            fullWidth
            autoComplete="cc-csc"
            value={formik.values.cvv}
            onChange={formik.handleChange}
            error={formik.errors.cvv} helperText={formik.errors.cvv}
          />
        </Grid>
        <Grid item xs={12}>
          <FormControlLabel
            control={<Checkbox color="secondary" name="saveCard" value="yes"/>}
            label="Remember credit card details for next time"
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
}
