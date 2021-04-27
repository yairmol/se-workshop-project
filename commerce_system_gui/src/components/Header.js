import React from 'react';
import PropTypes from 'prop-types';
import {makeStyles} from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import {Badge} from "@material-ui/core";
import AccountCircle from '@material-ui/icons/AccountCircle';
import NotificationsIcon from '@material-ui/icons/Notifications';

const useStyles = makeStyles((theme) => ({
  toolbar: {
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  toolbarButton:{
    margin: theme.spacing(1),
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
  },
}));

export default function Header(props) {
  const classes = useStyles();
  const {categories, title, signedIn, onSignUp} = props;

  return (
      <React.Fragment>
        <Toolbar className={classes.toolbar}>
          <Button variant="outlined" size="small">Subscribe</Button>
          <Typography
              component="h2"
              variant="h5"
              color="inherit"
              align="center"
              noWrap
              className={classes.toolbarTitle}
          >
            {title}
          </Typography>
          <IconButton>
            <SearchIcon/>
          </IconButton>
          {signedIn ? <>
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
          <Button variant="outlined" size="small" onClick={onSignUp} className={classes.toolbarButton}>
            Sign up
          </Button>
          <Button variant="outlined" size="small" onClick={onSignUp} className={classes.toolbarButton}>
            Sign in
          </Button>
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
                {category.title}
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
