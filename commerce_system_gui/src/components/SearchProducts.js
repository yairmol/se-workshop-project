import {Transaction} from "./Transaction";
import {
  Card,
  CardContent,
  CardHeader,
  CardMedia,
  FormControl,
  InputLabel,
  Select,
  TextField,
  Typography
} from "@material-ui/core";
import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Grid from '@material-ui/core/Grid';
import {
  get_all_categories,
  get_all_shops_ids_and_names,
  get_all_shops_info,
  get_all_user_names,
  get_system_transactions_of_shops,
  get_system_transactions_of_user,
  get_user_transactions, search_products
} from "../api";
import {useAuth} from "./use-auth";
import {Link} from "react-router-dom";
import IconButton from "@material-ui/core/IconButton";
import SearchIcon from "@material-ui/icons/Search";
import Divider from "@material-ui/core/Divider";
import {Link as RouteLink} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: 345,
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
  expand: {
    transform: 'rotate(0deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },

  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  mainFeaturedPost: {
    position: 'relative',
    // backgroundColor: theme.palette.grey[800],
    // color: theme.palette.common.white,
    marginBottom: theme.spacing(4),
    // backgroundImage: 'url(https://source.unsplash.com/random)',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: "100%",
  },
  overlay: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    // backgroundColor: 'rgba(0,0,0,.3)',
  },
  mainFeaturedPostContent: {
    position: 'relative',
    padding: theme.spacing(3),
    [theme.breakpoints.up('md')]: {
      padding: theme.spacing(6),
      paddingRight: 0,
    },
  },
  formControl: {
    margin: theme.spacing(2),
    minWidth: 200,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  searchButton: {
    margin: theme.spacing(3),
  },
}));

export default function SearchProducts() {
  const classes = useStyles();
  const [searchVal, setSearchVal] = useState("");
  const [fromPrice, setFromPrice] = useState(0);
  const [toPrice, setToPrice] = useState(Infinity);
  const [searchProducts, setSearchProducts] = useState([]);
  //   useState([{product_name: "p1",description: "a product", price: 1, quantity: 10, categories:[0,1]},
  // {product_name: "p2",description: "a product", price: 2.5, quantity: 10,
  // categories: [1,2]},]);
  const [categories, setCategories] = useState([]);
  const [allCategories, setAllCategories] = useState([]);
  const [keywords, setKeywords] = useState("");
  const auth = useAuth();

  const onCategoriesChange = (event, value) => {
    console.log(value);
    setCategories(value);
  }
  const handleSearchChange = (event) => {
    setSearchVal(event.target.value);
    auth.getToken().then((token) => {
      search_products(token, event.target.value, keywords, categories,
        [{type: "price_range", "from": fromPrice, "to": toPrice === Infinity ? Number.MAX_SAFE_INTEGER : toPrice}])
        .then((res) => {
          // alert(JSON.stringify(res))
          setSearchProducts(res)
        })
        .catch((err) => setSearchProducts(searchProducts))
    })
  }
  const handleFromChange = (event) => {
    const val = event.target.value;
    if (val === "") setFromPrice(0);
    else if (!Number.isNaN(val)) setFromPrice(parseInt(val));
  }
  const handleToChange = (event) => {
    const val = event.target.value;
    if (val === "" || Number.isNaN(parseInt(val))) setToPrice(0);
    else if (!Number.isNaN(parseInt(val))) setToPrice(parseInt(val));
  }

  useEffect(async () => {
    // await search_products(await auth.getToken(), searchVal, keywords, categories,[{"from": fromPrice, "to":toPrice}] )
    //     .then((res) => {
    //       alert(JSON.stringify(res))
    //       setSearchProducts(res || searchProducts)
    //     })
    //     .catch((err) => setSearchProducts(searchProducts))

    await get_all_categories(await auth.getToken())
      .then((res) => {
        setAllCategories(res || allCategories)
      })
      .catch((err) => setAllCategories(allCategories))
  }, [])

  return (
    <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <TextField id="standard-basic" label="Product Name" value={searchVal} onChange={handleSearchChange}
                     fullWidth/>
        </Grid>
        {/*</Grid>*/}
        {/*<Grid spacing = {4}container xs >*/}
        <Grid item xs={3}>
          <TextField id="from price" label="from" variant="outlined" value={fromPrice} onChange={handleFromChange}/>
          <TextField id="to price" label="to" variant="outlined" value={toPrice} onChange={handleToChange}/>
        </Grid>
        <Grid item xs>
          <Autocomplete
            multiple
            id="tags-standard"
            options={allCategories}
            onChange={onCategoriesChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                label="Categories"
                placeholder="Categories"
              />
            )}
          />
        </Grid>
      </Grid>
      <div style={{width: "100%", height: "2rem"}}/>
      <Grid items xs={10}>
        <Grid container justify="center" spacing={2}>
          <Divider/>
          {searchProducts.map((product) => (
            <Grid item>
              <RouteLink to={{pathname: `/shops/${product.shop_id}/products/${product.product_id}`, header: `Product: ${product.product_name}`}}>
                <Card className={classes.root}>
                  <CardHeader
                    title={product.product_name}
                  />
                  <CardMedia
                    className={classes.media}
                    image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-X2ZRp_vz2_Tg55J3pKupby0yJT-zG_xTw6cjjQ1ywFZ2j68_C3m1l-SCN4be_io4Vqw&usqp=CAU"
                  />
                  <CardContent>
                    <Typography variant="body2" color="textSecondary" component="p">
                      Product Price: {product.price}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" component="p">
                      Product Description: {product.description}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" component="p">
                      Product Quantity: {product.quantity}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" component="p">
                      Product Categories: {product.categories}
                    </Typography>
                  </CardContent>
                </Card>
              </RouteLink>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </>
  );
}