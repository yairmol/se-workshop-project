import {Input} from "@material-ui/core";
import React, {useEffect, useState} from "react";
import Button from "@material-ui/core/Button";
import ButtonBase from '@material-ui/core/ButtonBase';
import Typography from '@material-ui/core/Typography';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';

import {useAuth} from "./use-auth";
import {get_all_shops_info, get_user_transactions} from "../api";
import {Link} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
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
},];
export const Main_page = (props) => {
  const {searchQuery} = props;
  const [shops, setShops] = useState(shopData);
  const auth = useAuth();

  useEffect(async () => {
    await get_all_shops_info(await auth.getToken())
        .then((res) => {
          setShops(res.data || shopData)
        })
        .catch((err) => setShops(shopData))
  }, [])
  const filteredShops = shops.filter((shop) => shop.shop_name.toLowerCase().includes(searchQuery.toLowerCase()));
  console.log(filteredShops);
  return (
      <div>
        <Grid
        container
        spacing = {3}
        xl
          >
          {filteredShops.length > 0 ?  <ButtonBases shops ={filteredShops} /> :
           <Typography  color = "secondary" align="center" variant= "h3">There are no open shops  <br /> :( </Typography>}
        </Grid>
      </div>
  );
}
export default function ButtonBases({shops}){
  const classes = useStyles();
  const defaultImageUrl = "https://p1.hiclipart.com/preview/33/96/19/shopping-cart-red-line-material-property-logo-circle-vehicle-rectangle-png-clipart.jpg";
  console.log(shops[0].shopImage === "" ? defaultImageUrl : shops[0].shopImage);
  return (
    <div className={classes.root}>
      {shops.map((shop) =>
      <Grid item xs = {12} >
        <ButtonBase
          focusRipple
          key={shop.shop_id}
          className={classes.shopImage}
          focusVisibleClassName={classes.focusVisible}
          href={`/shop/${shop.shop_name}`}
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
      </Grid>
      )}
    </div>
  );
}
