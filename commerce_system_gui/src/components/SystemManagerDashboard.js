import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {useAuth} from "./use-auth";
import {useFormik} from "formik";
import Button from "@material-ui/core/Button";
import {MuiPickersUtilsProvider, KeyboardDatePicker, KeyboardTimePicker} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import TextField from "@material-ui/core/TextField";
import {get_stats} from "../api";
import {Paper, Typography} from "@material-ui/core";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { PieChart, Pie, Sector, Cell, ResponsiveContainer } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

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
  button: {
    minWidth: 'max-content',
  },
  searchButton: {
    margin: theme.spacing(3),
  },
  autoComplete: {
    maxWidth: 300
  }
}));

function UsersChart({stats}){
  const subscribed = stats.actions.login ? stats.actions.login.length : 0;
  const entered = stats.actions.enter ? stats.actions.enter.length : 0;
  const guests = entered - subscribed;
  const data = [
    {
      "name": "subscribed",
      "value": subscribed
    },
    {
      "name": "guests",
      "value": guests
    }
  ]
  return (
    <ResponsiveContainer width="100%" height="100%">
        <PieChart width={400} height={400}>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            // labelLine={true}
            // label={renderCustomizedLabel}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
  );
}

function ActionsChart(){
  return <Typography>Not implemented</Typography>
}

function Stats({stats}) {
  return (
    <Grid container>
      <Grid item xs={4}>
        <Paper>
          <UsersChart stats={stats}/>
        </Paper>
      </Grid>
      <Grid item xs={8}>
        <ActionsChart stats={stats}/>
      </Grid>
    </Grid>
  )
}

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

  const getStats = () => {
    const actions = formik.values.filterByActions ? formik.values.actions : null;
    const users = formik.values.filterByUsernames ? formik.values.usernames : null;
    const time_window = formik.values.filterByTimeStamp ? [formik.values.fromTS.valueOf(), formik.values.toTS.valueOf()] : null;
    alert(JSON.stringify(actions))
    alert(JSON.stringify(users))
    auth.getToken().then((token) =>
      get_stats(token, actions, users, time_window).then((_stats) => {
        alert(JSON.stringify(_stats))
        setStats(_stats)
      }))
  }

  useEffect(() => {
    function fetchData() {

    }

    fetchData();
  }, [auth])

  const onFilterByTimeStampClick = () => {
    formik.setValues({...formik.values, filterByTimeStamp: !formik.values.filterByTimeStamp})
  }

  const onFilterByUsernamesClick = () => {
    formik.setValues({...formik.values, filterByUsernames: !formik.values.filterByUsernames})
  }

  const onFilterByActionNameClick = () => {
    formik.setValues({...formik.values, filterByActions: !formik.values.filterByActions})
  }

  return (loaded &&
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Grid item xs={12}>
        <Grid container direction="column">
          <Grid item xs={12}>
            <Grid container spacing={3}>
              <Grid item>
                <Grid container direction="column" spacing={3}>
                  <Grid item>
                    <Button variant="outlined" className={classes.button}
                            onClick={onFilterByTimeStampClick}>
                      {formik.values.filterByTimeStamp && "Cancel "}Filter by Time
                    </Button>
                  </Grid>
                  {formik.values.filterByTimeStamp &&
                  <Grid item>
                    <KeyboardDatePicker format="dd/MM/yyyy" label="From Date" name="fromTS" variant="outlined"
                                        onChange={(date) => formik.handleChange({
                                          target: {
                                            name: "fromTS",
                                            value: date
                                          }
                                        })}
                                        value={formik.values.fromTS}
                                        KeyboardButtonProps={{'aria-label': 'change date'}}/>
                    <KeyboardDatePicker format="dd/MM/yyyy" label="To Date" name="toTS" variant="outlined"
                                        onChange={(date) => formik.handleChange({target: {name: "toTS", value: date}})}
                                        value={formik.values.toTS}
                                        KeyboardButtonProps={{'aria-label': 'change date'}}/>
                    {/*<KeyboardTimePicker KeyboardButtonProps={{'aria-label': 'change time'}}*/}
                    {/*                    label="From Time" name="" variant="outlined"*/}
                    {/*                    onChange={(date) => formik.handleChange({target: {name: value.key, value: date}})}*/}
                  </Grid>}
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
            <Grid container direction="row" justify="center">
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