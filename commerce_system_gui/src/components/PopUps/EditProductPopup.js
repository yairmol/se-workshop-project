import React, {useState} from "react";
import {
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  FormGroup, InputAdornment, TextField
} from "@material-ui/core";
import Button from "@material-ui/core/Button";
import NumberFormat from 'react-number-format';

//
// token: str
// shop_id: int
// product_id: int,
//     product_name: str
// description: str,
//             price: float,
//     quantity: int,
//     categories: List[str]


function NumberFormatCustom(props) {
  const { inputRef, onChange, ...other } = props;

  return (
    <NumberFormat
      {...other}
      getInputRef={inputRef}
      onValueChange={(values) => {
        onChange({
          target: {
            name: props.name,
            value: values.value,
          },
        });
      }}
      thousandSeparator
      isNumericString
    />
  );
}


export default function EditProductPopup({product, close_window_func, edit_product_func}) {
  const [open, setOpen] = useState(true)

  const [name, setName] = useState(product.product_name);
  const [price, setPrice] = useState(product.price);
  const [description, setDescription] = useState(product.description);
  const [categories, setCategories] = useState(product.categories);

  const set_categories = (category_str) => {
    let categories_lst = category_str.split(',');
    for (let i =0; i<categories_lst.length; i++) {
      categories_lst[i] = categories_lst[i].trim();
    }
    setCategories(categories_lst);
  }

  const get_categories = () => {
    let cat_str = categories[0]
    for (let i =1; i<categories.length; i++) {
      cat_str += ', ' + categories[i]
    }
    return cat_str
  }

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const done = () => {
    /*
    CALL FOR SET PERMISSIONS
     */
    edit_product_func(name, price, description, categories)
    handleClose()
  }

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Edit {product.product_name}
        </DialogTitle>
        <DialogContent>
        <form autoComplete="off">
            <TextField autoFocus margin="dense" id="name" label="product name" fullWidth defaultValue={name}
                       onChange={(e) => setName(e.target.value)} />
            <TextField autoFocus margin="dense" id="name" label="description" fullWidth defaultValue={description}
                       onChange={(e) => setPrice(e.target.value)} />
            <TextField autoFocus margin="dense" id="name" label="price" fullWidth defaultValue={price} InputProps={{
            startAdornment: <InputAdornment position="start">₪</InputAdornment>, inputComponent: NumberFormatCustom,
          }}           onChange={(e) => setDescription(e.target.value)}/>
            <TextField autoFocus margin="dense" id="name" label="categories" fullWidth
                       defaultValue={get_categories()}
                       onChange={(e) => set_categories(e.target.value)}/>
        </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={done} color="primary">
            Done
          </Button>
          <Button onClick={handleClose} color="primary" autoFocus>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
