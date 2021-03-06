import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Grid from '@material-ui/core/Grid';

const payments = [
  // { name: 'Card type', key: 'Visa' },
  { name: 'Card holder', key: 'cardName' },
  { name: 'Card number', key: 'cardNumber' },
  { name: 'Expiry date', key: 'expDate' },
];

const useStyles = makeStyles((theme) => ({
  listItem: {
    padding: theme.spacing(1, 0),
  },
  total: {
    fontWeight: 700,
  },
  title: {
    marginTop: theme.spacing(2),
  },
}));

export default function Review({formik, cart, shoppingBag}) {
  const classes = useStyles();
  const products = cart ?
          Object.keys(cart.shopping_bags).reduce(
              (prev, cur, i) => prev.concat(cart.shopping_bags[cur].products),
              []
          ) :
          shoppingBag.products;

  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Order summary
      </Typography>
      <List disablePadding>
        {products.map((product) => (
          <ListItem className={classes.listItem} key={product.product_name}>
            <ListItemText primary={product.product_name} secondary={product.description} />
            <Typography variant="body2">{product.purchase_price}₪</Typography>
          </ListItem>
        ))}
        <ListItem className={classes.listItem}>
          <ListItemText primary="Total" />
          <Typography variant="subtitle1" className={classes.total}>
            {cart ? cart.total : shoppingBag.total}₪
          </Typography>
        </ListItem>
      </List>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <Typography variant="h6" gutterBottom className={classes.title}>
            Shipping
          </Typography>
          <Typography gutterBottom>{formik.values.firstName} {formik.values.lastName}</Typography>
          <Typography gutterBottom>{[formik.values.address1, formik.values.address2].join(', ')}</Typography>
        </Grid>
        <Grid item container direction="column" xs={12} sm={6}>
          <Typography variant="h6" gutterBottom className={classes.title}>
            Payment details
          </Typography>
          <Grid container>
            {payments.map((payment) => (
              <React.Fragment key={payment.name}>
                <Grid item xs={6}>
                  <Typography gutterBottom>{payment.name}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography gutterBottom>{formik.values[payment.key]}</Typography>
                </Grid>
              </React.Fragment>
            ))}
          </Grid>
        </Grid>
      </Grid>
    </React.Fragment>
  );
}
