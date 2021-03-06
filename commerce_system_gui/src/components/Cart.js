import {
  Button,
  CircularProgress,
  TextField,
  IconButton,
  Link as MUILink,
  InputLabel,
  Select,
  MenuItem, FormControl
} from "@material-ui/core";
import React, {useCallback, useEffect, useState} from "react";
import {makeStyles} from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import AccordionActions from '@material-ui/core/AccordionActions';
import Divider from '@material-ui/core/Divider';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import {change_purchase_type, get_cart_info, remove_product_from_cart, save_product_to_cart} from "../api";
import {useAuth} from "./use-auth";
import RemoveCircleOutlineIcon from '@material-ui/icons/RemoveCircleOutline';
import {Link as RouteLink} from "react-router-dom";


const purchase_types_map = {
  'buy_now': 'Buy Now',
  'offer': 'Price Offer',
}


const columns = [
  {id: 'product_name', label: 'Name', getter: (p) => p['product_name']},
  {
    id: 'description',
    label: 'Description',
    getter: (p) => p['description']
    // minWidth: 170,
    // align: 'right',
  },
  {
    id: 'price',
    label: 'Base Price',
    getter: (p) => p['price']
    // minWidth: 170,
    // align: 'right',
  },
  {
    id: 'purchase_price',
    label: 'Purchasing Price',
    getter: (p) => p['purchase_price']
    // minWidth: 170,
    // align: 'right',
  },
  {
    id: 'amount',
    label: 'Quantity',
    minWidth: 170,
    getter: (p) => p['amount']
    // align: 'right',
  },
  {id: 'purchase_type', label: 'Purchase Type', getter: (p) => p.purchase_type.purchase_type}
];

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    marginTop: theme.spacing(3),
    alignItems: "center",
  },
  accordion: {
    width: '80%',
    margin: "auto",
    marginBottom: theme.spacing(1.5),
  },
  checkoutButton: {
    margin: 10,
    // padding: "0"
  },
  cartCheckoutButton: {
    marginLeft: "500px",
    marginRight: "5%",
    // padding: "0"
  },
  heading: {
    fontSize: theme.typography.pxToRem(19),
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  icon: {
    verticalAlign: 'bottom',
    height: 20,
    width: 20,
  },
  container: {
    maxHeight: 440,
  },
  details: {
    alignItems: 'center',
  },
  column: {
    flexBasis: '33.33%',
  },
  helper: {
    borderLeft: `2px solid ${theme.palette.divider}`,
    padding: theme.spacing(1, 2),
  },
  link: {
    color: theme.palette.primary.main,
    textDecoration: 'none',
    '&:hover': {
      textDecoration: 'underline',
    },
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 160,
  },
}));

function StickyHeadProductsTable({products, onProductChange, onRemoveProduct, onProductPTChange}) {
  const classes = useStyles();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const auth = useAuth();

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <Paper className={classes.root}>
      <TableContainer className={classes.container}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{minWidth: column.minWidth}}
                >
                  {column.label}
                </TableCell>
              ))}
              <TableCell key="remove-product" align="left">Remove product</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {products.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((product) =>
                <TableRow hover role="checkbox" tabIndex={-1} key={product.product_id}>
                  {columns.map((column) => {
                    const value = column.getter(product);
                    return (
                      <TableCell key={column.id} align={column.align}>
                        {column.id === "amount" ?
                          <TextField id="standard-number" label="Number" type="number" value={value}
                                     onChange={(event) =>
                                       onProductChange(product.product_id, event.target.value)}/> :
                           column.id === "purchase_type" ?
                             <FormControl required className={classes.formControl}>
                              <InputLabel id="purchase-type-label">{column.label}</InputLabel>
                              <Select labelId="purchase-type-label"
                                      id={column.id} label={column.label} name={column.id}
                                      onChange={(e) =>
                                        onProductPTChange(product.product_id, e.target.value)} value={value}>
                                {product.purchase_types.filter((pt) => !pt.for_subs_only || auth.user).map((pt) =>
                                  <MenuItem selected={pt.purchase_type === value} value={pt.purchase_type}>
                                    {purchase_types_map[pt.purchase_type]}
                                  </MenuItem>)}
                              </Select>
                            </FormControl> :
                          column.format && typeof value === 'number' ? column.format(value) : value
                        }
                      </TableCell>
                    );
                  })}
                  <TableCell key="remove-product">
                    <IconButton onClick={() => onRemoveProduct(product.product_id)}>
                      <RemoveCircleOutlineIcon/>
                    </IconButton>
                  </TableCell>
                </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={products.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
    </Paper>
  );
}

const ShoppingBagView = ({shopId, shoppingBag, refresh}) => {
  const classes = useStyles();
  const auth = useAuth();
  const [productsState, setProducts] = useState(JSON.parse(JSON.stringify(shoppingBag.products)));
  const [edited, setEdited] = useState(false);

  const onSaveChanges = useCallback((products) => {
    auth.getToken().then(async (token) => {
      if (products.length === 0) {
        await Promise.all(shoppingBag.products.map((product) =>
          remove_product_from_cart(token, shopId, product.product_id, product.amount)
        ))
        console.log("finished removing all products from cart")
      } else {
        let j = 0;  // new shoppingBag index
        for (let i = 0; i < shoppingBag.products.length; i++) {
          while (products[j].product_id !== shoppingBag.products[i].product_id) {
            await remove_product_from_cart(
              token, shopId, shoppingBag.products[i].product_id, shoppingBag.products[i].amount
            );
            i++;
            console.log(`finished removing product ${shoppingBag.products[i].product_id}`);
          }
          let func = (x) => x;
          const additional_amount = parseInt(products[j].amount) - parseInt(shoppingBag.products[i].amount);
          if (additional_amount > 0) {
            func = save_product_to_cart;
          } else if (additional_amount < 0) {
            func = remove_product_from_cart;
          }
          await func(token, shopId, products[j].product_id, Math.abs(additional_amount));
          console.log(`finished changing quantity of product ${shoppingBag.products[i].product_id}`);
          if (products[j].purchase_type.purchase_type !== shoppingBag.products[i].purchase_type.purchase_type) {
            const pt_args = products[j].purchase_type.purchase_type === 'offer' ? {offer_maker: auth.user} : {}
            await change_purchase_type(token, shopId, products[j].product_id, products[j].purchase_type.id, pt_args)
            console.log(`finished changing purchase type of product ${shoppingBag.products[i].product_id}`);
          }
          j++
        }
      }
      refresh();
    })
  }, [shopId, shoppingBag.products, refresh, auth])

  const onProductChange = (prod_id, val) => {
    if (val < 0) {
      alert("product amount can't be under 0");
      return
    }
    let product_idx = 0;
    for (let i = 0; i < productsState.length; i++) {
      if (productsState[i].product_id === prod_id) {
        product_idx = i;
        break;
      }
    }
    let product = productsState[product_idx]
    product.amount = val;
    setProducts([
      ...productsState.slice(0, product_idx),
      product,
      ...productsState.slice(product_idx + 1)
    ])
    setEdited(productsState !== shoppingBag.products);
  }

  const onProductPTChange = (prod_id, pt) => {
    const product_idx = productsState.findIndex((p) => p.product_id === prod_id);
    let product = {...productsState[product_idx]}
    product.purchase_type = product.purchase_types.find((other_pt) => other_pt.purchase_type === pt);
    setProducts([
      ...productsState.slice(0, product_idx),
      product,
      ...productsState.slice(product_idx + 1)
    ])
    setEdited(productsState !== shoppingBag.products);
  }

  const onRemoveProduct = (prod_id) => {
    let product_idx = 0;
    for (let i = 0; i < productsState.length; i++) {
      if (productsState[i].product_id === prod_id) {
        product_idx = i;
        break;
      }
    }
    setProducts([
      ...productsState.slice(0, product_idx),
      ...productsState.slice(product_idx + 1)
    ])
    setEdited(productsState !== shoppingBag.products);
  }

  const onCancel = () => {
    setProducts(JSON.parse(JSON.stringify(shoppingBag.products)));
    setEdited(false);
  }

  return (
    <div className={classes.accordion}>
        <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon/>}
          aria-controls="panel1c-content"
          id="panel1c-header"
        >
          <div className={classes.column}>
              <MUILink className={classes.heading}>Shopping Bag for {shoppingBag.shop_name}</MUILink>
            <Typography className={classes.secondaryHeading}>total: {shoppingBag.total}</Typography>
              {productsState.length > 0 &&
              <RouteLink to={{
                pathname: "/checkout",
                shop_id: shopId,
                from: "cart",
                header: "Checkout"
              }}>
                <Button color="primary" variant="outlined" className={classes.checkoutButton}>Checkout</Button>
              </RouteLink>}
          </div>
          <div className={classes.column}>
            {edited ? <Typography className={classes.secondaryHeading}>edited</Typography> : <></>}
          </div>
        </AccordionSummary>
        <AccordionDetails className={classes.details}>
            {productsState.length > 0 ?
                <StickyHeadProductsTable products={productsState} onProductChange={onProductChange}
                                         onProductPTChange={onProductPTChange} onRemoveProduct={onRemoveProduct}/>
                : <Typography>Shopping bag is empty</Typography>}
        </AccordionDetails>
        <Divider/>
        <AccordionActions>
          <Button size="small" onClick={onCancel}>Cancel</Button>
          <Button size="small" color="primary" onClick={() => onSaveChanges(productsState)}>
            Save
          </Button>
        </AccordionActions>
      </Accordion>
    </div>
  )
}

export const Cart = () => {
  const classes = useStyles();
  const auth = useAuth();
  const [loaded, setLoaded] = useState(false);
  const [cart, setCart] = useState({shopping_bags: {}});

  const refresh = () => {
    console.log("refreshing");
    setLoaded(false);
  }

  useEffect(() => {
    if (!loaded) {
      console.log("in cart use effect")
      auth.getToken().then((token) =>
        get_cart_info(token).then((res) => {
          if (res) {
            console.log(`cart ${JSON.stringify(res)}`);
            setCart(res);
          }
        })
      )
      setLoaded(true);
    }
  }, [loaded, auth]);

  return (
    <div className={classes.root}>
      {
        loaded ? Object.keys(cart.shopping_bags).map((sid) =>
            <ShoppingBagView shopId={sid} shoppingBag={cart.shopping_bags[sid]} refresh={refresh}/>)
          : <CircularProgress/>
      }
      {
        Object.keys(cart.shopping_bags).length === 0 ?
          <Typography align="center">
            You currently have no shopping bags, start shopping <RouteLink to={{pathname: "/", header: "Main"}}>here</RouteLink>
          </Typography> :
          <RouteLink to={{
            pathname: "/checkout",
            cart: true,
            from: "cart",
            header: "Checkout"
          }}>
            <Button className={classes.cartCheckoutButton} variant="contained" color="primary">Checkout Cart</Button>
          </RouteLink>
      }
    </div>
  );
};
