import React, {useState} from 'react';
import PropTypes from 'prop-types';
import {fade, makeStyles} from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import Typography from '@material-ui/core/Typography';
import {Link as RouteLink, useHistory} from 'react-router-dom';
import Link from '@material-ui/core/Link'
import {Badge, InputBase, Snackbar} from "@material-ui/core";
import AccountCircle from '@material-ui/icons/AccountCircle';
import NotificationsIcon from '@material-ui/icons/Notifications';
import {useAuth} from "./use-auth";
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';
import {Alert} from "@material-ui/lab";
import EmailIcon from '@material-ui/icons/Email';
import NotificationDrawer from "./notificationDrawer";

const useStyles = makeStyles((theme) => ({
  empty: {
    color: "gray",
  },
  toolbar: {
    borderBottom: `1px solid ${theme.palette.divider}`,
    alignItems: "center",
  },
  toolbarButton: {
    margin: theme.spacing(1),
    textDecoration: "none"
  },
  toolbarTitle: {
    flex: 1,
  },
  toolbarSecondary: {
    justifyContent: 'space-around',
    overflowX: 'auto',
    alignItems: "center",
    display: 'flex'
  },
  toolbarLink: {
    padding: theme.spacing(1),
    flexShrink: 0,
    color: "gray",
    textDecoration: "none",
  },
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
}));

export default function Header(props) {
  const classes = useStyles();
  const {categories, title} = props;
  const auth = useAuth();
  const history = useHistory();

  const [notifList, setNotifListData] = useState(["Hello", "Is this working ? ", "Maybe"]);
  const [notifSnackBarOpen, setNotifSnackBarOpen] = useState(false);
  const [notifDrawerOpen, setNotifDrawerOpen] = useState(false);

  const onNotifReceived = (msg) => {
        notifList.push(msg)
        setNotifListData(notifList);
        setNotifSnackBarOpen(true);
  }
  const handleCloseNotif = () => {
      setNotifSnackBarOpen(false);
  }
  const handleNotifClick = () => {
      setNotifDrawerOpen(true);
  }

  auth.registerNotifHandler(onNotifReceived);

  const signout = () => {
    auth.signout().then((res) => {
      if (res) {
        history.replace({pathname: "/login"})
      }
    })
  }
  return (
      <React.Fragment>
        <Toolbar className={classes.toolbar}>
          {/*<Button variant="outlined" size="small">Subscribe</Button>*/}
          <Typography
              component="h2"
              variant="h5"
              color="inherit"
              align="left"
              noWrap
              className={classes.toolbarTitle}
          >
            {title}
          </Typography>


           <RouteLink to="/products">
              <Button variant="outlined" size="small" className={classes.toolbarButton}>
                    Product Info
                  </Button>
          </RouteLink>

          <RouteLink to="/cart">
            <IconButton>
              <Badge badgeContent={0} color="secondary">
                <ShoppingCartIcon/>
              </Badge>
            </IconButton>
          </RouteLink>
          <RouteLink to="/shops/:shop_id/discounts">
            <Button variant="outlined" size="small" className={classes.toolbarButton}>
              discounts
            </Button>
          </RouteLink>
          {auth.user ? <>
                <Button variant="outlined" size="small" onClick={signout} className={classes.toolbarButton}>
                  Sign out
                </Button>
                <IconButton aria-label="show 17 new notifications" color="inherit">
                  <Badge badgeContent={0} color="secondary">
                    <NotificationsIcon/>
                  </Badge>
                </IconButton>
                <IconButton
                    edge="end"
                    aria-label="account of current user"
                    aria-haspopup="true"
                    color="inherit"
                >
                  <AccountCircle/>
                </IconButton></> :
              <div>
                <RouteLink to="/register" style={{textDecoration: "none"}}>
                  <Button variant="outlined" size="small" className={classes.toolbarButton}>
                    Sign up
                  </Button>
                </RouteLink>
                <RouteLink to="/login" style={{textDecoration: "none"}}>
                  <Button variant="outlined" size="small" className={classes.toolbarButton}>
                    Sign in
                  </Button>
                </RouteLink>
              </div>

          }
      <IconButton onClick={handleNotifClick}>
          <Badge badgeContent={notifList.length} color="secondary">
            <EmailIcon/>
          </Badge>
        </IconButton>
        </Toolbar>
        <Toolbar component="nav" variant="dense" className={classes.toolbarSecondary}>
          {categories.map((category) => (
              <Link
                  color="inherit"
                  noWrap
                  key={category.title}
                  variant="body2"
                  href={category.url}
                  className={classes.toolbarLink}
              >
                <RouteLink className={classes.toolbarLink} to={`/${category.url}`}>
                  {category.title}
                </RouteLink>
          </Link>

          ))}
        </Toolbar>
          <Snackbar open={notifSnackBarOpen} autoHideDuration={5000} onClose={handleCloseNotif}>
            <Alert severity="info">Received a new message</Alert>
          </Snackbar>
        <NotificationDrawer open={notifDrawerOpen} setOpen = {setNotifDrawerOpen} msgs = {notifList} setMsgs = {setNotifListData} />
      </React.Fragment>
  );
}

Header.propTypes = {
  sections: PropTypes.array,
  title: PropTypes.string,
};
