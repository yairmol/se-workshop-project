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
import {add_discount, get_shop_discounts, get_shop_info, move_discount_to, remove_discount} from "../api";
import {useAuth} from "./use-auth";
import {useParams} from "react-router-dom";

const conditionTypes = {
  "sum": "Total Price",
  "quantity": "Number of Products"
}

let nextid = 3;

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
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
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
  discount: {
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
  discountText: {
    fontSize: theme.typography.pxToRem(15),
  },
  discountText2: {
    fontSize: theme.typography.pxToRem(20),
  }
}));

function SimpleDiscount({discount, classname, productNames}) {
  const classes = useStyles();
  // alert(`identifier ${JSON.stringify(discount.target_identifier)}`)
  const parseCond = (cond) => {
    return `the ${conditionTypes[cond.condition] || "__"} of ${
      cond.type === "category" ? `all products of category ${cond.identifier || "__"}` :
        cond.type === "product" ? `product ${productNames[cond.identifier] || "__"}` :
          cond.type === "shop" ? "the entire shopping bag" : "__"
    } is more then ${cond.num || "__"}`
  }

  const parseList = (list) => {
    const operator = list[0];
    return list.slice(1).map((condition, i) =>
      `${i > 0 ? `${operator} ` : ""}${condition instanceof Array ? `(${parseList(condition)})` :
        condition instanceof Object ? parseCond(condition) : ""}`)
  };

  const has_cond = (discount.condition instanceof Array && discount.condition.length > 0) ||
    (!(discount.condition instanceof Array) && discount.condition !== {})

  // alert(JSON.stringify(discount))

  return (
    <>
      <Typography variant="h6" className={classes[classname]}>
        {discount.percentage || "__"}% discount on
        {discount.type === "product" ? ` ${productNames[discount.identifier] || "__"}` :
          discount.type === "category" ? ` all products from ${discount.identifier || "__"}` :
            discount.type === "shop" ? " on the entire shop!" : "__"}
      </Typography>
      <Typography>
        {has_cond && `if ${discount.condition instanceof Array ? parseList(discount.condition) :
          discount.condition instanceof Object ? parseCond(discount.condition) : ""}`}
      </Typography>
    </>
  )
}

function CompositeDiscount({discount, onDrop, removeDiscount, productNames}) {
  const classes = useStyles();

  const [collected, drop] = useDrop(() => ({
    accept: "DISCOUNT",
    drop: (item, monitor) => onDrop(discount.id, item, monitor)
  }));

  return (
    <div ref={drop}>
      <Typography>{discount.operator}</Typography>
      <List>
        {discount.discounts.map((discount, index) => (
          <ListItem>
            <DiscountView productsNames={productNames} onDrop={onDrop} removeDiscount={removeDiscount} discount={discount} index={index}
                          key={discount.id}/>
          </ListItem>
        ))}
      </List>
      <div className={classes.dropHere}>Drop Discounts Here</div>
    </div>
  )
}

function DiscountView({discount, index, onDrop, removeDiscount, productsNames}) {
  const classes = useStyles();
  const [{isDragging}, drag, dragPreview] = useDrag(
    () => ({
      type: "DISCOUNT",
      item: {id: discount.id},
      collect: (monitor) => ({
        isDragging: monitor.isDragging()
      })
    }),
    []
  )

  return (
    <div className={classes.root2} role="Handle" ref={drag} style={{opacity: 1}}>
      <Paper style={{maxHeight: 500, overflow: 'auto'}} className={classes.discount} elevation={2}>
        {/*<DragHandleIcon/>*/}
        {!discount.composite ?
          <SimpleDiscount discount={discount} classname={"discountText"} productNames={productsNames}/> :
          <CompositeDiscount removeDiscount={removeDiscount} discount={discount} onDrop={onDrop}
                             productNames={productsNames}/>}
        <IconButton onClick={() => removeDiscount(discount)}>
          <DeleteIcon/>
        </IconButton>
      </Paper>
    </div>
  )
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

export const Discounts = () => {
  const classes = useStyles();
  const [discounts, setDiscounts] = useState([]);
  const [shop, setShop] = useState({products: []});
  const product_id_to_name = {}
  shop.products.forEach((prod, i) => {
    product_id_to_name[prod.product_id] = prod.product_name;
  })
  const [loaded, setLoaded] = useState(false);
  const [addComp, setAddComp] = useState(null);
  const auth = useAuth();
  const {shop_id} = useParams();
  // alert(JSON.stringify(discounts))
  useEffect(() => {
    if (!loaded) {
      auth.getToken().then((token) =>
        get_shop_info(token, shop_id).then((shopInfo) =>
          get_shop_discounts(token, shop_id).then((discounts) => {
            setShop(shopInfo);
            setDiscounts(discounts);
            setLoaded(true);
          })
        )
      )
    }
  })

  const saveDiscount = async (discount) => {
    // alert(`saving discount ${JSON.stringify(discount)}`);
    const has_cond = !!(discount.conditions && discount.conditions.length > 0);
    // alert(JSON.stringify(parseCondition(discount.conditions, discount.rators)))

    add_discount(
      await auth.getToken(), shop.shop_id, has_cond, discount,
      discount.conditions ? parseCondition(discount.conditions, discount.rators, true) : null
    ).then((res) => {
      discounts.push(discount)
      setDiscounts(discounts);
      setLoaded(false);
      // forceUpdate();
    })
  }

  const removeDiscount = async (discount) => {
    remove_discount(
      await auth.getToken(), shop.shop_id, discount.id,
    ).then((res) => {
      setLoaded(false);
      // forceUpdate();
    })
    // forceUpdate();
  }

  const onDrop = async (droppableId, item, monitor) => {
    // alert(`discounts ${JSON.stringify(discounts)}`)
    move_discount_to(await auth.getToken(), shop_id, item.id, droppableId).then((res) => {
      setLoaded(false)
    })

    // const newDiscounts = moveItem(discounts, item.id, droppableId)
    // setDiscounts(newDiscounts)
    // forceUpdate();
    // move(path)
  }

  return (
    loaded ?
      <div>
        <DiscountForm shop={shop} saveDiscount={saveDiscount} productNames={product_id_to_name}/>
        <Divider style={{color: "black", margin: 20}}/>
        <Grid container className={classes.root} spacing={2} style={{marginBottom: 100}}>
          <Grid item>
            <Typography variant="h5">Compose Discounts</Typography>
          </Grid>
          <div style={{width: "100%"}}/>
          <Grid item xs={9}>
            <Grid container>
              <DndProvider backend={HTML5Backend}>
                {discounts.map((discount, index) => (
                  <Grid item>
                    <DiscountView discount={discount} index={index} key={discount.id} productsNames={product_id_to_name}
                                  onDrop={(d, i, m) => onDrop(d, i, m)} removeDiscount={removeDiscount}/>
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
                      saveDiscount({composite: true, operator: addComp, discounts: []});
                      nextid++;
                      setAddComp(null);
                    }} variant="outlined" color="primary" className={classes.submit}>Add</Button>
                  </Grid>
                </> :
                <Grid item>
                  <Button color="primary" className={classes.submit}
                          onClick={() => setAddComp("additive")} variant="outlined">Add Discount Composition
                    Rule
                  </Button>
                </Grid>}
            </Grid>
          </Grid>
        </Grid>
      </div> :
      <Typography>Loading...</Typography>
  )
};

function DiscountForm({shop, saveDiscount, productNames}) {
  const classes = useStyles();
  const [conditions, setConditions] = useState([]);
  const [rators, setRators] = useState([]);
  const formik = useFormik({
    initialValues: {
      type: '',
      percentage: '',
      identifier: '',
      composite: false,
    },
    onSubmit: values => {
      // alert(JSON.stringify(values))
      saveDiscount({
        id: nextid, ...values,
        conditions: conditions, rators: rators,
      })
      formik.setValues({
        type: '',
        percentage: '',
        identifier: '',
      })
      nextid++;
      setConditions([])
      setRators([])
    },
  });

  // alert(JSON.stringify(formik.values))

  function onConditionChange(e) {
    // alert(JSON.stringify(e.target))
    const [i, key] = e.target.name.split('-');
    conditions[i][key] = e.target.value;
    setConditions([...conditions]);
  }

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

  const onAddCondition = () => {
    setConditions([...conditions, {condition: '', type: '', identifier: '', num: ''}])
    setRators([...rators, 'and'])
  }

  const removeCondition = (i) => {
    setConditions([
      ...conditions.slice(0, i),
      ...conditions.slice(i + 1)
    ])
    if (i > 0) {
      setRators([
        ...rators.slice(0, i - 1),
        ...rators.slice(i)
      ])
    }
  }

  return (
    <form onSubmit={formik.handleSubmit} className={classes.form} noValidate>
      <Grid container direction={"row"} justify="center" className={classes.root} spacing={2}>
        <Grid item xs={8}>
          <Grid container spacing={2}>
            <Grid item>
              <Typography align="center" variant="h5">Add Simple Discount</Typography>
            </Grid>
            <div style={{width: "100%"}}/>
            <Grid item>
              <FormControl variant="outlined" required className={classes.formControl}>
                <InputLabel id="discount-target-label">Discount Target</InputLabel>
                <Select labelId="discount-target-label"
                        id="type" label="Discount Target" name="type" autoFocus
                        onChange={formik.handleChange} value={formik.values.type}>
                  <MenuItem value={"category"}>Category</MenuItem>
                  <MenuItem value={"product"}>Product</MenuItem>
                  <MenuItem value={"shop"}>Entire shop</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item>
              <FormControl disabled={formik.values.type === ''}
                           variant="outlined" required className={classes.formControl}>
                <InputLabel id="discount-target-identifier-label">{formik.values.type}</InputLabel>
                <Select
                  labelId="discount-target-identifier-label"
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
            {conditions && conditions.map((cond, i) =>
              <>{i > 0 &&
              <Grid item>
                <FormControl variant="outlined" required className={classes.formControl}>
                  <InputLabel id={`${i}-operator-label`}>Operator</InputLabel>
                  <Select labelId={`${i}-operator-label`}
                          id={`${i}-operator`} label="Operator" name={`${i}-operator`} autoFocus
                          onChange={(e) => setRators([...rators.slice(0, i - 1), e.target.value, ...rators.slice(i)])}
                          value={rators[i - 1]}>
                    <MenuItem value={"and"}>And</MenuItem>
                    <MenuItem value={"or"}>Or</MenuItem>
                  </Select>
                </FormControl>
              </Grid>}
                <Grid item>
                  <FormControl variant="outlined" required className={classes.formControl}>
                    <InputLabel id={`${i}-condition-type-label`}>Condition Type</InputLabel>
                    <Select labelId={`${i}-condition-type-label`}
                            id={`${i}-conditionType`} label="Condition Type" name={`${i}-condition`} autoFocus
                            onChange={onConditionChange} value={cond.condition}>
                      {Object.keys(conditionTypes).map((key) => <MenuItem value={key}>{conditionTypes[key]}</MenuItem>)}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item>
                  <FormControl variant="outlined" required className={classes.formControl}>
                    <InputLabel id={`${i}-condition-target-label`}>Condition Target</InputLabel>
                    <Select labelId={`${i}-condition-target-label`}
                            id={`${i}-conditionTarget`} label="Condition Target" name={`${i}-type`}
                            onChange={onConditionChange} value={cond.type}>
                      {cond.condition === "sum" || <MenuItem value={"product"}>Product</MenuItem>}
                      <MenuItem value={"category"}>Category</MenuItem>
                      {cond.condition === "quantity" || <MenuItem value={"shop"}>Entire Shopping bag</MenuItem>}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item>
                  <FormControl disabled={cond.type === ''}
                               variant="outlined" required className={classes.formControl}>
                    <InputLabel id={`${i}-condition-target-identifier-label`}>{cond.type} identifier</InputLabel>
                    <Select
                      labelId={`${i}-condition-target-identifier-label`}
                      id={`${i}-identifier`} label={`${cond.type} identifier`} name={`${i}-identifier`}
                      onChange={onConditionChange}
                      value={cond.identifier}
                    >
                      {getItems(cond.type)}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item>
                  <FormControl className={classes.formControl} required>
                    <TextField name={`${i}-num`} label="price" variant="outlined" id={`${i}-num`}
                               onChange={onConditionChange} value={cond.num}/>
                  </FormControl>
                </Grid>
                <Grid item>
                  <Button type="button" variant="outlined" color="primary"
                          className={classes.submit} onClick={() => removeCondition(i)}>Remove Condition</Button>
                </Grid>
                <div style={{width: "100%"}}/>
              </>)
            }
            <div style={{width: "100%"}}/>
            <Grid item>
              <Button
                type="button"
                fullWidth
                variant="outlined"
                color="primary"
                className={classes.submit}
                onClick={onAddCondition}
              >
                Add Condition
              </Button>
            </Grid>
            <Grid item>
              <Button
                type="submit"
                fullWidth
                variant="outlined"
                color="primary"
                className={classes.submit}
              >
                Save Simple Discount
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={4}>
          <Grid container spacing={2}>
            <Paper className={classes.discount} elevation={2}>
              <Grid item>
                Preview: <SimpleDiscount productNames={productNames} classname={classes.discountText2} discount={{
                ...formik.values, condition: parseCondition(conditions, rators)
              }}/>
              </Grid>
              <div style={{width: "100%"}}/>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
    </form>
  );
}
