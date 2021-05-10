import {Transaction} from "./Transaction";
import {FormControl, InputLabel, Select, TextField, Typography} from "@material-ui/core";
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

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
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

export default function Search_products() {
  const classes = useStyles();
  const [searchVal, setSearchVal] = useState("");
  const [fromPrice, setFromPrice] = useState(0);
  const [toPrice, setToPrice] = useState(0);
  const [searchProducts, setSearchProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [allCategories, setAllCategories] = useState(["!","@","#"]);
  const [keywords, setKeywords] = useState("");
  const auth = useAuth();

  const onCategoriesChange = (event, value ) => {
     console.log(value);
     setCategories(value);
  }
  const handleSearchChange = (event) => {
    setSearchVal(event.target.value);
  }
  const handleFromChange = (event) => {
    const val = event.target.value ;
    if(val === "") setFromPrice(0);
    else if (!Number.isNaN(val) ) setFromPrice(parseInt(val));
  }
  const handleToChange = (event) => {
    const val = event.target.value ;
    if(val === "") setToPrice(0);
    else if (!Number.isNaN(val) ) setToPrice(parseInt(val));
  }

  useEffect(async () => {
    await search_products(await auth.getToken(), searchVal, keywords, categories,[{"from": fromPrice, "to":toPrice}] )
        .then((res) => {
          setSearchProducts(res || searchProducts)
        })
        .catch((err) => setSearchProducts(searchProducts))

    await get_all_categories(await auth.getToken())
        .then((res) => {
          setAllCategories(res || allCategories)
        })
        .catch((err) => setAllCategories(allCategories))
  }, [])

  return (
      <div className={classes.root}>
        <Grid container spacing = {4}>
          <Grid item xs = {12}>
              <TextField id="standard-basic" label="Product Name" value = {searchVal} onChange={handleSearchChange} fullWidth/>
          </Grid>
        {/*</Grid>*/}
        {/*<Grid spacing = {4}container xs >*/}
          <Grid item xs = {3}>
            <TextField id="from price" label="from" variant="outlined" value = {fromPrice} onChange={handleFromChange}/>
            <TextField id="to price" label="to" variant="outlined" value = {toPrice} onChange={handleToChange}/>
          </Grid>
          <Grid item xs >
              <Autocomplete
              multiple
              id="tags-standard"
              options={allCategories}
              onChange={onCategoriesChange}
              renderInput={(params) => (
                  <TextField
                    {...params}
                    variant="standard"
                    label="Multiple values"
                    placeholder="Categories"
                  />
                )}
              />
          </Grid>
        </Grid>
        <Divider />

      </div>
  );
}