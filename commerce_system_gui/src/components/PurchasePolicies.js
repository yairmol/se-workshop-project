import React, {useEffect, useState} from "react";
import {makeStyles} from "@material-ui/core/styles";
import {useFormik} from "formik";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import {
  FormControl,
  IconButton,
  InputLabel,
  List,
  ListItem,
  MenuItem,
  Paper,
  Select,
  Typography
} from "@material-ui/core";
import Divider from "@material-ui/core/Divider";
import {useDrag, useDrop} from "react-dnd";
import {HTML5Backend} from 'react-dnd-html5-backend'
import {DndProvider} from 'react-dnd'
import DeleteIcon from '@material-ui/icons/Delete';
import {add_policy, get_shop_policies, get_shop_info, move_policy_to, remove_policy} from "../api";
import {useAuth} from "./use-auth";
import {useParams} from "react-router-dom";

const conditionTypes = {
  "sum": "Total Price",
  "quantity": "Number of Products"
}

function getPolicyPath(policies, id) {
  for (let i = 0; i < policies.length; i++) {
    if (id === policies[i].id) {
      return [i];
    } else if (policies[i].type === "composite") {
      const path = getpolicyPath(policies[i].policies, id);
      if (path) {
        return [i, ...path];
      }
    }
  }
  return null;
}

const getFromPath = (policies, path) => {
  let a = policies;
  for (let i = 0; i < path.length - 1; i++) {
    if (i === 0) {
      a = a[path[i]]
    } else {
      a = a.policies[path[i]]
    }
  }
  return a[path[path.length - 1]]
}

const remove = (policies, path) => {
  let a = policies;
  for (let i = 0; i < path.length - 1; i++) {
    a = a[path[i]].policies
  }
  const [removed] = a.splice(path[path.length - 1], 1)
  return removed
}

const add = (policy, policies, path) => {
  let a = policies;
  for (let i = 0; i < path.length; i++) {
    a = a[path[i]].policies
  }
  a.push(policy)
}

const moveItem = (policies, policyId, destId) => {
  const oldPath = getPolicyPath(policies, policyId)
  const policy = remove(policies, oldPath);
  const newPath = getPolicyPath(policies, destId)
  add(policy, policies, newPath)

  return policies;
};

let nextid = 1;

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  control: {
    padding: theme.spacing(2),
  },
  paper: {
    // marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'row',
    // alignItems: 'center',
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 160,
  },
  policy: {
    padding: theme.spacing(2),
    width: "auto",
    maxWidth: theme.spacing(48),
  },
  root2: {
    margin: theme.spacing(0),
    display: 'flex',
    flexWrap: 'wrap',
    '& > *': {
      margin: theme.spacing(0.5),
      width: "match-content",
    },
  },
  dropHere: {
    border: '1px dashed gray',
    padding: theme.spacing(2),
    margin: theme.spacing(1),
    cursor: 'move',
    float: 'left',
  },
  policyText: {
    fontSize: theme.typography.pxToRem(15),
  },
  policyText2: {
    fontSize: theme.typography.pxToRem(20),
  }
}));

function SimplePolicy({policy, classname}) {
  const classes = useStyles();

  return (
    <>
      <Typography variant="h6" className={classes[classname]}>
        {policy.percentage || "__"}% policy on
        {policy.type === "product" ? ` ${policy.identifier || "__"}` :
          policy.type === "category" ? ` all products from ${policy.identifier || "__"}` :
            policy.type === "shop" ? " on the entire shop!" : "__"}
      </Typography>
    </>
  )
}

function CompositePolicy({policy, onDrop, removePolicy}) {
  const classes = useStyles();

  const [collected, drop] = useDrop(() => ({
    accept: "POLICY",
    drop: (item, monitor) => onDrop(policy.id, item, monitor)
  }));

  return (
    <div ref={drop}>
      <Typography>{policy.operator}</Typography>
      <List>
        {policy.policies.map((policy, index) => (
          <ListItem>
            <PolicyView onDrop={onDrop} removePolicy={removePolicy} policy={policy} index={index}
                          key={policy.id}/>
          </ListItem>
        ))}
      </List>
      <div className={classes.dropHere}>Drop Policys Here</div>
    </div>
  )
}

function PolicyView({policy, index, onDrop, removePolicy}) {
  const classes = useStyles();
  const [{isDragging}, drag, dragPreview] = useDrag(
    () => ({
      type: "POLICY",
      item: {id: policy.id},
      collect: (monitor) => ({
        isDragging: monitor.isDragging()
      })
    }),
    []
  )

  return (
    <div className={classes.root2} role="Handle" ref={drag} style={{opacity: 1}}>
      <Paper style={{maxHeight: 500, overflow: 'auto'}} className={classes.policy} elevation={2}>
        {!policy.composite ?
          <SimplePolicy policy={policy} classname={"policyText"}/> :
          <CompositePolicy removePolicy={removePolicy} policy={policy} onDrop={onDrop}/>}
        <IconButton onClick={() => removePolicy(policy)}>
          <DeleteIcon/>
        </IconButton>
      </Paper>
    </div>
  )
}

function useForceUpdate() {
  const [value, setValue] = useState(0); // integer state
  return () => setValue(value => value + 1); // update the state to force render
}

const parseCondition = (conditions, rators, sendToApi) => {
  if (conditions.length === 0) {
    return []
  }
  if (conditions.length === 1) {
    return sendToApi ? [conditions[0]] : conditions[0]
  }
  return [
    rators[0], conditions[0], parseCondition(conditions.slice(1), rators.slice(1))
  ]
}

export const PurchasePolicies = () => {
  const classes = useStyles();
  const {shop_id} = useParams();
  const [policies, setPolicies] = useState([]);
  const [shop, setShop] = useState({products: []});
  const [loaded, setLoaded] = useState(false);
  const [addComp, setAddComp] = useState(null);
  const auth = useAuth();
  const forceUpdate = useForceUpdate();

  useEffect(() => {
    if (!loaded) {
      auth.getToken().then(async (token) => {
        await get_shop_info(token, shop_id).then((shopInfo) => {
          setShop(shopInfo);
        })
        await get_shop_policies(token, shop_id).then((policies) => {
          setPolicies(policies);
        })
        setLoaded(true);
      })
    }
  })

  const savePolicy = (policy) => {
    auth.getToken().then((token) => {
      add_policy(token, shop.shop_id, policy).then((res) => {
        policies.push(policy)
        setPolicies(policies);
        setLoaded(false);
        // forceUpdate();
      })
    })
  }

  const removePolicy = (policy) => {
    auth.getToken().then((token) => {
      remove_policy(token, shop.shop_id, policy.id).then((res) => {
        setLoaded(false);
      })
    })
  }

  const onDrop = async (droppableId, item, monitor) => {
    auth.getToken().then((token) => {
      move_policy_to(token, shop_id, item.id, droppableId).then((res) => {
        setLoaded(false)
      })
    })

    // const newDiscounts = moveItem(discounts, item.id, droppableId)
    // setDiscounts(newDiscounts)
    // forceUpdate();
    // move(path)
  }

  return (
    loaded ?
      <div>
        <PolicyForm shop={shop} savePolicy={savePolicy}/>
        <Divider style={{color: "black", margin: 20}}/>
        <Grid container className={classes.root} spacing={2} style={{marginBottom: 100}}>
          <Grid item>
            <Typography variant="h5">Compose Policies</Typography>
          </Grid>
          <div style={{width: "100%"}}/>
          <Grid item xs={9}>
            <Grid container>
              <DndProvider backend={HTML5Backend}>
                {policies.map((policy, index) => (
                  <Grid item>
                    <PolicyView policy={policy} index={index} key={policy.id}
                                  onDrop={(d, i, m) => onDrop(d, i, m)} removePolicy={removePolicy}/>
                  </Grid>
                ))}
              </DndProvider>
            </Grid>
          </Grid>
          <Grid item xs={3}>
            <Grid container direction={"row"} justify="center">
              {addComp ?
                <>
                  <Grid item>
                    <FormControl variant="outlined" required className={classes.formControl}>
                      <InputLabel id="comp-type-label">Composition type</InputLabel>
                      <Select labelId="comp-type-label"
                              id="comp-type" label="Composition type" name="comp-type" autoFocus
                              onChange={(e) => setAddComp(e.target.value)} value={addComp}>
                        <MenuItem value={"additive"}>Additive</MenuItem>
                        <MenuItem value={"max"}>Max</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item>
                    <Button onClick={() => {
                      savePolicy({composite: true, operator: addComp, policies: []});
                      nextid++;
                      setAddComp(null);
                    }} variant="outlined" color="primary" className={classes.submit}>Add</Button>
                  </Grid>
                </> :
                <Grid item>
                  <Button color="primary" className={classes.submit}
                          onClick={() => setAddComp("additive")} variant="outlined">Add Policy Composition Rule
                  </Button>
                </Grid>}
            </Grid>
          </Grid>
        </Grid>
      </div> :
      <Typography>Loading...</Typography>
  )
};

function PolicyForm({shop, savePolicy}) {
  const classes = useStyles();
  const formik = useFormik({
    initialValues: {
      type: '',
      composite: false,
    },
    onSubmit: values => {
      savePolicy({
        id: nextid, ...values,
      })
      formik.setValues({
        type: '',
      })
      nextid++;
    },
  });

  const getItems = (type) => {
    return type === "product" ?
      shop.products.map((p) => <MenuItem value={p.product_id}>{p.product_name}</MenuItem>) :
      type === "category" ?
        Array.from(new Set(shop.products.reduce((prev, curr, i) => prev.concat(curr.categories), [])
        )).map((c) => <MenuItem value={c}>{c}</MenuItem>) :
        type === "shop" ?
          <MenuItem selected={true} value={shop.shop_id}>{shop.shop_name}</MenuItem> :
          null
  }

  return (
    <form onSubmit={formik.handleSubmit} className={classes.form} noValidate>
      <Grid container direction={"row"} justify="center" className={classes.root} spacing={2}>
        <Grid item xs={8}>
          <Grid container spacing={2}>
            <Grid item>
              <Typography align="center" variant="h5">Add Simple Policy</Typography>
            </Grid>
            <div style={{width: "100%"}}/>
            <Grid item>
              <FormControl variant="outlined" required className={classes.formControl}>
                <InputLabel id="policy-type-label">Policy Type</InputLabel>
                <Select labelId="policy-type-label"
                        id="type" label="Policy type" name="type" autoFocus
                        onChange={formik.handleChange} value={formik.values.type}>
                  <MenuItem value={"tbd"}>Dont know</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item>
              <FormControl disabled={formik.values.type === ''}
                           variant="outlined" required className={classes.formControl}>
                <InputLabel id="policy-target-identifier-label">{formik.values.type}</InputLabel>
                <Select
                  labelId="policy-target-identifier-label"
                  id="identifier" label={formik.values.type} name="identifier"
                  onChange={formik.handleChange}
                  value={formik.values.identifier}
                >
                  {getItems(formik.values.type)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item>
              <FormControl className={classes.formControl} required>
                <TextField name="percentage" label="percentage" variant="outlined" id="percentage"
                           onChange={formik.handleChange} value={formik.values.percentage}/>
              </FormControl>
            </Grid>
            <div style={{width: "100%"}}/>
            <Grid item>
              <Button
                type="submit"
                fullWidth
                variant="outlined"
                color="primary"
                className={classes.submit}
              >
                Save Simple Policy
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={4}>
          <Grid container spacing={2}>
            <Paper className={classes.policy} elevation={2}>
              <Grid item>
                Preview: <SimplePolicy classname={classes.policyText2} policy={formik.values}/>
              </Grid>
              <div style={{width: "100%"}}/>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
    </form>
  );
}
