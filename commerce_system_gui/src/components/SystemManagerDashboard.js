import React, {useCallback, useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {useAuth} from "./use-auth";
import {useFormik} from "formik";
import Button from "@material-ui/core/Button";
import {MuiPickersUtilsProvider, KeyboardDatePicker, KeyboardTimePicker} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import TextField from "@material-ui/core/TextField";
import {get_stats} from "../api";
import {Link, ListItem, Paper, Tooltip, Typography} from "@material-ui/core";
import Autocomplete from "@material-ui/lab/Autocomplete";
import ActionsChart from "./ActionsChart";
import UsersChart from "./UsersChart";
import List from "@material-ui/core/List";

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
    margin: theme.spacing(1),
    minWidth: 100,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  button: {
    minWidth: 'max-content',
  },
  searchButton: {
    margin: theme.spacing(3),
  },
  autoComplete: {
    maxWidth: 300
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
}));

function Stats({stats}) {
  const classes = useStyles();
  const actions = stats.actions;
  const actions_done = Object.keys(actions).map((key) => ({action: key, num: actions[key].length}))
  const subscribers = stats.actions.login ? stats.actions.login.length : 0;
  const entered = stats.actions.enter ? stats.actions.enter.length : 0;
  const users_data = [
    {
      "name": "subscribers",
      "value": subscribers,
    },
    {
      "name": "guests",
      "value": entered - subscribers,
    }
  ]
  return (
    <Grid container spacing={3}>
      <Grid item xs={4}>
        <Paper className={classes.paper}>
          <Typography variant="h5">
            Guests and Users demography
          </Typography>
          <UsersChart data={users_data}/>
        </Paper>
      </Grid>
      <Grid item xs={8}>
        <Paper className={classes.paper}>
          <Typography variant="h5">
            Number of Actions Performed
          </Typography>
          <ActionsChart actions={actions_done}/>
        </Paper>
      </Grid>
    </Grid>
  )
}


const unitToMilliseconds = {
  "m": 60 * 1000,
  "h": 60 * 60 * 1000,
  "d": 24 * 60 * 60 * 1000,
  "M": 30 * 24 * 60 * 60 * 1000,
}

const timeRanges = [
  {
    label: "Last 10 minutes",
    value: "10",
    unit: "m",
  },
  {
    label: "Last 30 minutes",
    value: "30",
    unit: "m",
  },
  {
    label: "Last Hour",
    value: "1",
    unit: "h",
  },
  {
    label: "Last 6 Hours",
    value: "6",
    unit: "h",
  },
  {
    label: "Last Day (24 Hours)",
    value: "1",
    unit: "d",
  },
  {
    label: "Last Week",
    value: "7",
    unit: "d",
  },
  {
    label: "Last Month",
    value: "1",
    unit: "M",
  },
]

export default function SystemManagerDashboard() {
  const classes = useStyles();
  const auth = useAuth();
  const [stats, setStats] = useState({actions: [], users: [], action_names: []});
  const [loaded, setLoaded] = useState(false);
  const users = stats.users;
  const action_names = stats.action_names;

  const formik = useFormik({
    initialValues: {
      filterByTimeStamp: false,
      fromTS: new Date(),
      toTS: new Date(),
      filterByUsernames: false,
      usernames: [],
      filterByActions: false,
      actions: []
    },
    onSubmit: values => {
    },
  });

  const onSystemEvent = useCallback((record) => {
    console.log(`system event ${JSON.stringify(record)}`);
    const newStats = {...stats};
    if (stats.users.includes(record.action_maker)){
      newStats.users.push(record.action_maker)
    }
    if (!stats.action_names.includes(record.action)){
      newStats.action_names.push(record.action)
    }
    if (!Object.keys(stats.actions).includes(record.action)){
      console.log(`action ${record.action} is not in ${JSON.stringify(Object.keys(stats.actions))}`)
      newStats.actions[record.action] = []
    }
    newStats.actions[record.action].push(record)
    console.log(`actions ${JSON.stringify(newStats.actions[record.action])}`)
    setStats(newStats);
  }, [stats])

  const getStats = useCallback(() => {
    const actions = formik.values.filterByActions ? formik.values.actions : null;
    const users = formik.values.filterByUsernames ? formik.values.usernames : null;
    const time_window = formik.values.filterByTimeStamp ? [formik.values.fromTS.valueOf() / 1000, formik.values.toTS.valueOf() / 1000] : null;
    auth.getToken().then((token) =>
      get_stats(token, actions, users, time_window).then((_stats) => {
        setStats(_stats)
        setLoaded(true)
        auth.registerSystemEventHandler(onSystemEvent);
      }))
  }, [auth, formik.values.actions, formik.values.filterByActions, formik.values.filterByUsernames,
    formik.values.filterByTimeStamp, formik.values.fromTS, formik.values.toTS, formik.values.usernames, onSystemEvent])

  useEffect(() => {
    console.log('in system useeffect')
    if (!loaded) {
      function fetchData() {
        getStats()
      }

      fetchData();
    }
  }, [auth, getStats])

  const onFilterByTimeStampClick = () => {
    formik.setValues({...formik.values, filterByTimeStamp: !formik.values.filterByTimeStamp})
  }

  const onFilterByUsernamesClick = () => {
    formik.setValues({...formik.values, filterByUsernames: !formik.values.filterByUsernames})
  }

  const onFilterByActionNameClick = () => {
    formik.setValues({...formik.values, filterByActions: !formik.values.filterByActions})
  }

  const timeWindowToDate = (timeWindow) => {
    const currentDate = new Date();
    return new Date(currentDate.getTime() - unitToMilliseconds[timeWindow.unit] * timeWindow.value);
  }

  return (loaded &&
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Grid item xs={12}>
        <Grid container direction="column">
          <Grid item xs={12}>
            <Grid container spacing={3}>
              <Grid item>
                <Grid container direction="column">
                  <Grid item>
                    <Button variant="outlined" className={classes.button}
                            onClick={onFilterByTimeStampClick}>
                      {formik.values.filterByTimeStamp && "Cancel "}Filter by Time
                    </Button>
                  </Grid>
                  {formik.values.filterByTimeStamp &&
                  <Grid item>
                    <Grid container direction="row">
                      <Grid item direction="column">
                        <Grid item>
                          <KeyboardDatePicker format="dd/MM/yyyy" label="From Date" name="fromTS" variant="outlined"
                                              onChange={(date) => {
                                                const newDate = formik.values.fromTS;
                                                newDate.setDate(date.getDate())
                                                alert(newDate.getTime() / 1000)
                                                formik.setValues({
                                                  ...formik.values, fromTS: newDate
                                                })
                                              }}
                                              value={formik.values.fromTS} className={classes.formControl}
                                              KeyboardButtonProps={{'aria-label': 'change date'}}/>
                        </Grid>
                        <Grid item>
                          <KeyboardTimePicker KeyboardButtonProps={{'aria-label': 'change time'}}
                                              label="From Time" name="" variant="outlined"
                                              className={classes.formControl}
                                              onChange={(date) => {
                                                const newDate = formik.values.fromTS;
                                                newDate.setTime(date.getTime())
                                                alert(newDate.getTime() / 1000)
                                                formik.setValues({
                                                  ...formik.values, fromTS: newDate
                                                })
                                              }} value={formik.values.fromTS}/>
                        </Grid>
                      </Grid>
                      <Grid item direction="column">
                        <Grid item>
                          <KeyboardDatePicker format="dd/MM/yyyy" label="To Date" name="toTS" variant="outlined"
                                              onChange={(date) => {
                                                const newDate = formik.values.toTS;
                                                newDate.setDate(date.getDate())
                                                alert(newDate.getTime() / 1000)
                                                formik.setValues({
                                                  ...formik.values, toTS: newDate
                                                })
                                              }}
                                              value={formik.values.toTS} className={classes.formControl}
                                              KeyboardButtonProps={{'aria-label': 'change date'}}/>
                        </Grid>
                        <Grid item>
                          <KeyboardTimePicker KeyboardButtonProps={{'aria-label': 'change time'}}
                                              label="From Time" name="" variant="outlined"
                                              className={classes.formControl}
                                              onChange={(date) => {
                                                const newDate = formik.values.toTS;
                                                newDate.setTime(date.getTime())
                                                alert(newDate.getTime() / 1000)
                                                formik.setValues({
                                                  ...formik.values, toTS: newDate
                                                })
                                              }} value={formik.values.toTS}/>
                        </Grid>
                      </Grid>
                    </Grid>
                  </Grid>}
                  {formik.values.filterByTimeStamp &&
                    <List>
                      {timeRanges.map((timeWindow, index) =>
                        <ListItem key={index}>
                          <Link onClick={() => formik.setValues({
                            ...formik.values, fromTS: timeWindowToDate(timeWindow), toTS: new Date()
                          })}>
                            {timeWindow.label}
                          </Link>
                        </ListItem>)
                      }
                    </List>
                  }
                </Grid>
              </Grid>
              <Grid item>
                <Grid container direction="column" spacing={3}>
                  <Grid item>
                    <Button variant="outlined" className={classes.button}
                            onClick={onFilterByUsernamesClick}>
                      {formik.values.filterByUsernames && "Cancel "}Filter by Username
                    </Button>
                  </Grid>
                  {formik.values.filterByUsernames &&
                  <Grid item>
                    <Autocomplete className={classes.autoComplete}
                                  multiple
                                  options={users}
                                  onChange={(e, v) => {
                                    formik.handleChange({target: {name: "usernames", value: v}})
                                  }}
                                  name="usernames"
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      variant="standard"
                                      name="usernames"
                                      label="usernames"
                                      placeholder="usernames"
                                    />
                                  )}
                    />
                  </Grid>}
                </Grid>
              </Grid>
              <Grid item>
                <Grid container direction="column" spacing={3}>
                  <Grid item>
                    <Button variant="outlined" className={classes.button}
                            onClick={onFilterByActionNameClick}>
                      {formik.values.filterByActions && "Cancel "}Filter Actions
                    </Button>
                  </Grid>
                  {formik.values.filterByActions &&
                  <Grid item>
                    <Autocomplete
                      multiple
                      options={action_names}
                      onChange={(e, v) => {
                        formik.handleChange({target: {name: "actions", value: v}})
                      }}
                      name="actions"
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="standard"
                          name="actions"
                          label="actions"
                          placeholder="actions"
                        />
                      )}
                    />
                  </Grid>}
                </Grid>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12}>
            <Grid container direction="row" justify="center" style={{marginBottom: 10}}>
              <Button color="primary" variant="outlined" className={classes.button}
                      onClick={getStats}>
                Get Stats
              </Button>
            </Grid>
          </Grid>
          <Grid item xs={12}>
            <Stats stats={stats}/>
          </Grid>
        </Grid>
      </Grid>
    </MuiPickersUtilsProvider>
  );
}