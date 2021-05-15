import {Input, InputBase} from "@material-ui/core";
import React, {useEffect, useState} from "react";
import Button from "@material-ui/core/Button";
import ButtonBase from '@material-ui/core/ButtonBase';
import Typography from '@material-ui/core/Typography';
import {fade, makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';

import {useAuth} from "./use-auth";
import {get_all_shops_info, get_user_transactions} from "../api";
import SearchIcon from "@material-ui/icons/Search";
import {Link as RouteLink} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  search: {
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: fade(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing(2),
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing(3),
      width: 'auto',
    },
  },
  searchIcon: {
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  inputRoot: {
    color: 'inherit',
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    minWidth: 300,
    width: '100%',
  },
  shopImage: {
    position: 'relative',
    height: 200,
    [theme.breakpoints.down('xs')]: {
      width: '100% !important', // Overrides inline-style
      height: 100,
    },
    '&:hover, &$focusVisible': {
      zIndex: 1,
      '& $imageBackdrop': {
        opacity: 0.15,
      },
      '& $imageMarked': {
        opacity: 0,
      },
      '& $imageTitle': {
        border: '4px solid currentColor',
      },
    },
  },
  focusVisible: {},
  imageButton: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: theme.palette.common.white,
  },
  imageSrc: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    backgroundSize: 'cover',
    backgroundPosition: 'center 40%',
  },
  imageBackdrop: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    backgroundColor: theme.palette.common.black,
    opacity: 0.4,
    transition: theme.transitions.create('opacity'),
  },
  imageTitle: {
    position: 'relative',
    padding: `${theme.spacing(2)}px ${theme.spacing(4)}px ${theme.spacing(1) + 6}px`,
  },
  imageMarked: {
    height: 3,
    width: 18,
    backgroundColor: theme.palette.common.white,
    position: 'absolute',
    bottom: -2,
    left: 'calc(50% - 9px)',
    transition: theme.transitions.create('opacity'),
  },
}));
const shopData = [{
  shop_name: "Burger Shop",
  description: "desc",
  shop_id: "1",
  shopImage: "https://media1.s-nbcnews.com/i/newscms/2019_21/2870431/190524-classic-american-cheeseburger-ew-207p_d9270c5c545b30ea094084c7f2342eb4.jpg",
},
{
  shop_name: "Shoe Shop",
  description: "desc",
  shop_id: "2",
  shopImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSl1bzkA2J0UpyeDJTG1PqbYOqOJE4o-AAvw&usqp=CAU",
},
{
  shop_name: "Flower Shop",
  description: "desc",
  shop_id: "3",
  shopImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVocyW9xaVWyWJKH1IF9VOQDqXCyK6wTdB0Q&usqp=CAU",
},
];
export const MainPage = (props) => {
  const classes = useStyles();
  const [shops, setShops] = useState(shopData);
  const auth = useAuth();
  const [searchQuery, setSearchQuery] = useState("");

  function onSearchChange(event){
    // event.persist();
    console.log( event.target.value);
    setSearchQuery(event.target.value);
  }
  useEffect(() => {
     auth.getToken().then((token) => {
         get_all_shops_info(token).then((res) => {
           setShops(res)
         }).catch((err) => setShops(shopData))
       }
     )
  }, [])
  const filteredShops = shops.filter((shop) => shop.shop_name.toLowerCase().includes(searchQuery.toLowerCase()));
  console.log(filteredShops);
  return (
      <>

        <Grid
        container
        spacing = {4}
        xl
          >
          <Grid item>
           <div className={classes.search}>
            <div className={classes.searchIcon}>
              <SearchIcon/>
            </div>
            <InputBase
                placeholder="Search…"
                fullWidth
                classes={{
                  root: classes.inputRoot,
                  input: classes.inputInput,
                }}
                onChange={onSearchChange}
                inputProps={{'aria-label': 'search'}}
            />
          </div>
            </Grid>
          {filteredShops.length > 0 ?  <ButtonBases shops ={filteredShops} /> :
           <Typography  color = "secondary" align="center" variant= "h3">There are no open shops  <br /> :( </Typography>}
        </Grid>
      </>
  );
}
export default function ButtonBases({shops}){
  const classes = useStyles();
  const defaultImageUrl = "https://p1.hiclipart.com/preview/33/96/19/shopping-cart-red-line-material-property-logo-circle-vehicle-rectangle-png-clipart.jpg";
  return (
    <div className={classes.root}>
      {shops.map((shop,ind) =>
       (
           <>
             <Grid item xs >
        <RouteLink to={{pathname: `/shops/${shop.shop_id}`, header: `Shop: ${shop.shop_name}`}}>
          <ButtonBase
          focusRipple
          key={shop.shop_id}
          className={classes.shopImage}
          focusVisibleClassName={classes.focusVisible}
          style={{
            width: '100%',
          }}
        >
          <span
            className={classes.imageSrc}
            style={{

              backgroundImage: `url(${shop.shopImage === "" ? defaultImageUrl : shop.shopImage})`,
            }}
          />
          <span className={classes.imageBackdrop} />
          <span className={classes.imageButton}>
            <Typography
              component="span"
              variant="subtitle1"
              color="inherit"
              className={classes.imageTitle}
            >
              {shop.shop_name}
              <span className={classes.imageMarked} />
            </Typography>
          </span>
        </ButtonBase>
        </RouteLink>
     </Grid></>)

      )}
    </div>
  );
}
