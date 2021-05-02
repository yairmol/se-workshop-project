import React from 'react';
import PropTypes from 'prop-types';
import {makeStyles} from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import Typography from '@material-ui/core/Typography';
import {Link as RouteLink, useHistory} from 'react-router-dom';
import Link from '@material-ui/core/Link'
import {Badge} from "@material-ui/core";
import AccountCircle from '@material-ui/icons/AccountCircle';
import NotificationsIcon from '@material-ui/icons/Notifications';
import {useAuth} from "./use-auth";

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
}));

export default function Header(props) {
  const classes = useStyles();
  const {categories, title} = props;
  const auth = useAuth();
  const history = useHistory();

  const signout = () => {
    auth.signout().then((res) => {
      if (res) {
        history.replace({ pathname: "/login" })
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
          <IconButton>
            <SearchIcon/>
          </IconButton>
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
              </div>}
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
                <RouteLink className={classes.toolbarLink} to={`/categories/${category.url}`}>
                  {category.title}
                </RouteLink>
              </Link>

          ))}
        </Toolbar>
      </React.Fragment>
  );
}

Header.propTypes = {
  sections: PropTypes.array,
  title: PropTypes.string,
};
