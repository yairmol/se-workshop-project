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
import {add_policy, get_shop_policies, get_shop_info, remove_purchase_policy} from "../api";
import {useAuth} from "./use-auth";
import {useParams} from "react-router-dom";
import {MuiPickersUtilsProvider, KeyboardDatePicker, KeyboardTimePicker} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";

const condition_types = [
  {key: "max_quantity_for_product_condition", text: "Max Quantity on Product"},
  {key: "time_window_for_category_condition", text: "Purchase Time Window For Category"},
  {key: "time_window_for_product_condition", text: "Purchase Time Window For Product"},
  {key: "date_window_for_category_condition", text: "Purchase Date Window For Category"},
  {key: "date_window_for_product_condition", text: "Purchase Date Window For Product"},
]

const condition_types_dict = {
  "max_quantity_for_product_condition": "Max Quantity on Product",
  "time_window_for_category_condition": "Purchase Time Window For Category",
  "time_window_for_product_condition": "Purchase Time Window For Product",
  "date_window_for_category_condition": "Purchase Date Window For Category",
  "date_window_for_product_condition": "Purchase Date Window For Product",
}

function formatDate(date) {
  return date ? date instanceof Date ? `${date.getUTCDate()}/${date.getMonth() + 1}/${date.getFullYear()}` : date : "__"
}

function formatTime(date){
  return date ? date instanceof Date ? `${date.getHours()}:${date.getMinutes()}` : date : "__"
}

const condition_type_to_format_str = {
  "max_quantity_for_product_condition": (p, pr_names) => `product ${pr_names[p.product] || "__"} with a quantity less than ${p.max_quantity || "__"}`,
  "time_window_for_category_condition": (p, _) => `products from category ${p.category || "__"} between ${formatTime(p.min_time)} and ${formatTime(p.max_time)}`,
  "time_window_for_product_condition": (p, pr_names) => `product ${pr_names[p.product] || "__"} between ${formatTime(p.min_time)} and ${formatTime(p.max_time)}`,
  "date_window_for_category_condition": (p, _) => `products from category ${p.category || "__"} between ${formatDate(p.min_date)} and ${formatDate(p.max_date)}`,
  "date_window_for_product_condition": (p, pr_names) => `product ${pr_names[p.product] || "__"} between ${formatDate(p.min_date)} and ${formatDate(p.max_date)}`,
}

const ct_to_f = {
  "max_quantity_for_product_condition": {
    "product": {key: "product", text: "Product", type: "select"},
    "max_quantity": {key: "max_quantity", text: "Max Quantity", type: "text_field"}
  },
  "time_window_for_category_condition": {
    "category": {key: "category", text: "Category", type: "select"},
    "min_time": {key: "min_time", text: "Start Time", type: "time"},
    "max_time": {key: "max_time", text: "End Time", type: "time"}
  },
  "time_window_for_product_condition": {
    "product": {key: "product", text: "Product", type: "select"},
    "min_time": {key: "min_time", text: "Start Time", type: "time"},
    "max_time": {key: "max_time", text: "End Time", type: "time"}
  },
  "date_window_for_category_condition": {
    "category": {key: "category", text: "Category", type: "select"},
    "min_date": {key: "min_date", text: "Start Date", type: "date"},
    "max_date": {key: "max_date", text: "End Date", type: "date"}
  },
  "date_window_for_product_condition": {
    "product": {key: "product", text: "Product", type: "select"},
    "min_date": {key: "min_date", text: "Start Date", type: "date"},
    "max_date": {key: "max_date", text: "End Date", type: "date"},
  },
}

const time_policy_formatter = (policy) => ({
  ...policy,
  min_time: formatTime(policy.min_time),
  max_time: formatTime(policy.max_time)
})

const date_policy_formatter = (policy) => ({
  ...policy,
  min_date: formatDate(policy.min_date),
  max_date: formatDate(policy.max_date)
})

const ct_to_formatter = {
  "max_quantity_for_product_condition": (policy) => policy,
  "time_window_for_category_condition": time_policy_formatter,
  "time_window_for_product_condition": time_policy_formatter,
  "date_window_for_category_condition": date_policy_formatter,
  "date_window_for_product_condition": date_policy_formatter,
}


function isComposite(p) {
  return p.condition_type === "and_condition" || p.condition_type === "or_condition"
}

function maxId(policies) {
  // alert(JSON.stringify(policies))
  const ret = Math.max(0, ...policies.map(
    (p) => {
      // alert(`pid ${p.id} ${parseInt(p.id)}`)
      return isComposite(p) ? Math.max(parseInt(p.id), maxId(p.conditions)) : parseInt(p.id)
    }
  ))
  // alert(JSON.stringify(`ret ${ret}`))
  return ret
}

function getPolicyPath(policies, id) {
  for (let i = 0; i < policies.length; i++) {
    if (id === policies[i].id) {
      return [i];
    } else if (isComposite(policies[i])) {
      const path = getPolicyPath(policies[i].conditions, id);
      if (path) {
        return [i, ...path];
      }
    }
  }
  return null;
}

const remove = (policies, path) => {
  let a = policies;
  for (let i = 0; i < path.length - 1; i++) {
    a = a[path[i]].conditions
  }
  const [removed] = a.splice(path[path.length - 1], 1)
  return removed
}

const add = (policy, policies, path) => {
  let a = policies;
  for (let i = 0; i < path.length; i++) {
    a = a[path[i]].conditions
  }
  a.push(policy)
}

const moveItem = (policies, policyId, destId) => {
  const oldPath = getPolicyPath(policies, policyId)
  // alert(oldPath);
  const policy = remove(policies, oldPath);
  const newPath = getPolicyPath(policies, destId)
  // alert(newPath)
  add(policy, policies, newPath)

  return policies;
};

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
    // resize: "both",
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
  },
  resizeConsumer: {
    display: "inline-flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "centerl",
    width: "auto",
    height: "auto",
    resize: "both",
    overflow: "hidden",
  }
}))

function SimplePolicy({policy, classname, productNames}) {
  const classes = useStyles();
  // alert(`${JSON.stringify(condition_types_dict[policy.condition_type])}, ${JSON.stringify(!!condition_types_dict[policy.condition_type])}`)
  return (condition_types_dict[policy.condition_type] ?
      <Typography variant="h6" className={classes[classname]}>
        Customer can only buy {condition_type_to_format_str[policy.condition_type](policy, productNames)}
      </Typography> :
      <Typography>Choose policy type</Typography>
  )
}

const composite_policies = {
  and_condition: "And",
  or_condition: "Or"
}

function CompositePolicy({policy, onDrop, removePolicy, productNames}) {
  const classes = useStyles();
  const [collected, drop] = useDrop(() => ({
    accept: "POLICY",
    drop: (item, monitor) => onDrop(policy.id, item, monitor)
  }));

  return (
    <div>
      <Grid container spacing={2}>
        <Grid item>
          <Typography>{composite_policies[policy.condition_type]}</Typography>
        </Grid>
        {policy.conditions.map((policy, index) => (
          <Grid item>
            <PolicyView onDrop={onDrop} removePolicy={removePolicy} policy={policy} index={index}
                        key={policy.id} productNames={productNames}/>
          </Grid>
        ))}
      </Grid>
      <Grid item ref={drop} className={classes.dropHere}>Drop Policys Here</Grid>
    </div>
  )
}

function PolicyView({policy, index, onDrop, removePolicy, productNames}) {
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
    // <ResizeConsumer
    //   className={classes.resizeConsumer}
    //   onSizeChanged={handleSizeChanged}>
    <div className={classes.root2} role="Handle" ref={drag} style={{opacity: 1}}>
      <Paper style={{maxHeight: 500, overflow: 'auto'}} className={classes.policy} elevation={2}>
        {policy.conditions instanceof Array ?
          <CompositePolicy removePolicy={removePolicy} policy={policy} onDrop={onDrop} productNames={productNames}/> :
          <SimplePolicy policy={policy} classname={"policyText"} productNames={productNames}/>}
        <IconButton onClick={() => removePolicy(policy)}>
          <DeleteIcon/>
        </IconButton>
      </Paper>
    </div>
    // </ResizeConsumer>
  )
}

function useForceUpdate() {
  const [value, setValue] = useState(0); // integer state
  return () => setValue(value => value + 1); // update the state to force render
}

export const PurchasePolicies = () => {
  const classes = useStyles();
  const {shop_id} = useParams();
  const [policies, setPolicies] = useState([]);
  const [orig_policies, setOrigPolicies] = useState([]);
  // alert(JSON.stringify(policies));
  const [shop, setShop] = useState({products: []});
  const productNames = {}
  shop.products.forEach((prod, i) => {
    productNames[prod.product_id] = prod.product_name;
  })
  const [loaded, setLoaded] = useState(false);
  const [addComp, setAddComp] = useState(null);
  const [nextId, setNextId] = useState(1);
  const [edited, setEdited] = useState(false);
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
          setOrigPolicies(JSON.parse(JSON.stringify(policies)));
          const Id = maxId(policies)
          setNextId(Id + 1)
        })
        setLoaded(true);
        setEdited(false);
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

  const addPolicy = (policy) => {
    policies.push({...policy, id: nextId})
    setPolicies(policies);
    setNextId(nextId + 1);
    setEdited(policies !== orig_policies);
    forceUpdate();
  }

  const removePolicy = (policy) => {
    const oldPath = getPolicyPath(policies, policy.id)
    // alert(oldPath);
    remove(policies, oldPath);
    setPolicies(policies);
    setEdited(policies !== orig_policies);
    forceUpdate();

    // auth.getToken().then((token) => {
    //   remove_purchase_policy(token, shop.shop_id, policy.id).then((res) => {
    //     setLoaded(false);
    //   })
    // })
  }

  const onDrop = async (droppableId, item, monitor) => {
    // alert(`on drop ${item.id} ${droppableId}`)
    const newPolicies = moveItem(policies, item.id, droppableId)
    setPolicies(newPolicies)
    setEdited(policies !== orig_policies);
    forceUpdate();
  }

  const saveChanges = () => {
    auth.getToken().then((token) =>
      Promise.all(orig_policies.map((policy) => remove_purchase_policy(token, shop_id, policy.id))).then((res) =>
        Promise.all(policies.map((policy) => add_policy(token, shop_id, policy))).then((res) =>
          setLoaded(false)
        )
      )
    )
  }

  // alert(JSON.stringify(policies))

  return (
    loaded ?
      <Grid container>
        <Grid item xs={12}>
          <Grid container direction="column">
            <Grid item xs={12}>
              <PolicyForm shop={shop} savePolicy={savePolicy} productNames={productNames}/>
            </Grid>
            <Divider style={{color: "black", margin: 20}}/>
            <Grid item xs={12}>
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
                          <PolicyView policy={policy} index={index} key={policy.id} productNames={productNames}
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
                              <MenuItem value={"and_condition"}>And</MenuItem>
                              <MenuItem value={"or_condition"}>Or</MenuItem>
                            </Select>
                          </FormControl>
                        </Grid>
                        <Grid item>
                          <Button onClick={() => {
                            addPolicy({conditions: [], condition_type: addComp});
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
                {edited &&
                  <Grid item xs={3}>
                    <Button className={classes.submit} color="primary" variant="outlined" onClick={saveChanges}>
                      Save
                    </Button>
                  </Grid>
                }
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid> :
      <Typography>Loading...</Typography>
  )
};

function PolicyForm({shop, savePolicy, productNames}) {
  const classes = useStyles();
  const formik = useFormik({
    initialValues: {
      condition_type: '',
    },
    onSubmit: values => {
      savePolicy(ct_to_formatter[values.condition_type](values))
      formik.setValues({
        condition_type: '',
      })
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
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
    <form onSubmit={formik.handleSubmit} className={classes.form} noValidate>
      <Grid container className={classes.root} spacing={2}>
        <Grid item xs={8}>
          <Grid container spacing={2} style={{width: "100%"}}>
            <Grid item>
              <Typography align="center" variant="h5">Add Simple Policy</Typography>
            </Grid>
            <div style={{width: "100%"}}/>
            <Grid item>
              <FormControl variant="outlined" required className={classes.formControl}>
                <InputLabel id="policy-type-label">Policy Type</InputLabel>
                <Select labelId="policy-type-label"
                        id="condition_type" label="Policy type" name="condition_type" autoFocus
                        onChange={formik.handleChange} value={formik.values.condition_type}>
                  {condition_types.map((ct) => <MenuItem value={ct.key}>{ct.text}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            {condition_types_dict[formik.values.condition_type] ?
              Object.entries(ct_to_f[formik.values.condition_type]).map(([key, value]) => {
                // alert(JSON.stringify(value))
                return <Grid item>
                  <FormControl variant="outlined" required className={classes.formControl}>
                    {value.type === "select" ? <>
                        <InputLabel id={`policy-${value.key}-label`}>{value.text}</InputLabel>
                        <Select
                          labelId={`policy-${value.key}-label`}
                          id={value.key} label={value.text} name={value.key}
                          onChange={formik.handleChange}
                          value={formik.values[value.key]}
                        >
                          {getItems(value.key)}
                        </Select></> :
                      value.type === "text_field" ?
                        <TextField labelId={`policy-${value.key}-label`} id={value.key} label={value.text}
                                   name={value.key} variant="outlined"
                                   onChange={formik.handleChange} value={formik.values[value.key]}/> :
                        value.type  === "date" ?
                          <KeyboardDatePicker format="dd/MM/yyyy" labelId={`policy-${value.key}-label`} id={value.key}
                                              label={value.text} name={value.key} variant="outlined"
                                              onChange={(date) => formik.handleChange({target: {name: value.key, value: date}})}
                                              value={formik.values[value.key]}
                                              KeyboardButtonProps={{'aria-label': 'change date'}}/> :
                          value.type === "time" ?
                            <KeyboardTimePicker KeyboardButtonProps={{'aria-label': 'change time'}}
                                                labelId={`policy-${value.key}-label`} id={value.key}
                                                label={value.text} name={value.key} variant="outlined"
                                                onChange={(date) => formik.handleChange({target: {name: value.key, value: date}})}
                                                value={formik.values[value.key]}/> :
                        <Typography>Bad type</Typography>
                    }
                  </FormControl>
                </Grid>
              }) : <Grid item>
                <div style={{width: "100%"}}/>
              </Grid>
            }
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
                Preview: <SimplePolicy classname={classes.policyText2} policy={formik.values}
                                       productNames={productNames}/>
              </Grid>
              <div style={{width: "100%"}}/>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
    </form>
    </MuiPickersUtilsProvider>
  );
}
