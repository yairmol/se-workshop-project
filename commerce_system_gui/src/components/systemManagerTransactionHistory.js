import {Transaction} from "./Transaction";
import {FormControl, InputLabel, Select, TextField, Typography} from "@material-ui/core";
import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Grid from '@material-ui/core/Grid';
import {
    get_all_shops_ids_and_names,
    get_all_user_names,
    // get_system_transactions_of_shops,
    // get_system_transactions_of_user,
} from "../api";
import {useAuth} from "./use-auth";
import IconButton from "@material-ui/core/IconButton";
import SearchIcon from "@material-ui/icons/Search";

const useStyles = makeStyles((theme) => ({
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
// e
export default function SystemManagerTransactionHistory() {
  const classes = useStyles();
  const [allUserNames, setAllUserNames] = useState( []);
  const [allShopNames, setAllShopNames] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [nameOf, setNameOf] = useState("User");
  const [name, setName] = useState("");
  // const [transactions, setTransactions] = useState([]);
  const transactions = [];
  const auth = useAuth();


  const onNameChange = (event, value) => {
      console.log(value);
      value === null ? setName("") : setName(value);
  }
  const onNameOfChange = (event) => {
      setNameOf(event.target.value)
  }

  // const onSearchClick = async () => {
  //     nameOf === "User" ?
  //     await get_system_transactions_of_user(await auth.getToken(), name)
  //       .then((res) => {
  //         setTransactions(res || [])
  //       })
  //       .catch((err) => setTransactions([])) :
  //     await get_system_transactions_of_shops(await auth.getToken(), name.id)
  //       .then((res) => {
  //         setTransactions(res || [])
  //       })
  //       .catch((err) => setTransactions([]))
  // }

  useEffect( () => {
    async function fetchData() {
      const token = await auth.getToken();
      await get_all_user_names(token)
        .then((res) => {
          setAllUserNames(res || [])
        })
        .catch((_) => setAllUserNames([]))
      await get_all_shops_ids_and_names(token)
        .then((res) => {
          setAllShopNames(res || [])
        })
        .catch((_) => setAllShopNames([]))
      setLoaded(true);
    }
    fetchData();
  }, [auth])

  return(loaded &&
      <Grid container >
        <Grid item xs = {3}>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="nameOf">get transaction history of</InputLabel>
            <Select
              native
              value={nameOf}
              onChange={onNameOfChange}
              inputProps={{
                name: 'nameOf',
                id: 'nameOf',
              }}
            >
              <option value={"Shop"}>Shop</option>
              <option value={"User"}>User</option>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs = {8}>
           <Autocomplete
            options = {nameOf === "User" ? allUserNames : allShopNames }
            getOptionLabel={(option) => nameOf === "User" ? option : option.name}
            id="clear-on-escape"
            clearOnEscape
            renderInput={(params) => <TextField {...params} label="Name" margin="normal" />}
            onChange={onNameChange}
            />
        </Grid>
          <Grid item xs = {1}>
              <IconButton aria-label="search" disabled = {name === ""} className={classes.searchButton}>
                  <SearchIcon />
              </IconButton>
          </Grid>
          <>
        <Grid item lg={6}>
          {(transactions && transactions.length > 0) ?
              transactions.map((transaction, index) => <Transaction key={index} transaction={transaction}/>)
              : <Typography align="center">To see the transactions, select a user or shop name</Typography>
          }
        </Grid></>
      </Grid>

  ) ;
}