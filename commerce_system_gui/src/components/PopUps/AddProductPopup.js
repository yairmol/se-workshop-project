import React, {useState} from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  InputAdornment, TextField
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


export default function AddProductPopup({close_window_func, add_product_func}) {
  const [open, setOpen] = useState(true)

  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [description, setDescription] = useState("");
  const [categories, setCategories] = useState("");
  const [quantity, setQuantity] = useState("");

  const set_categories = (category_str) => {
    let categories_lst = category_str.split(',');
    for (let i =0; i<categories_lst.length; i++) {
      categories_lst[i] = categories_lst[i].trim();
    }
    setCategories(categories_lst);
  }

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const done = () => {
    /*
    CALL FOR ADD PRODUCT
     */
    add_product_func(name, price, quantity, description, categories)
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
          Add product
        </DialogTitle>
        <DialogContent>
        <form autoComplete="off">
            <TextField autoFocus margin="dense" id="name" label="product name" fullWidth value={name}
                       onChange={(e) => setName(e.target.value)} />
            <TextField autoFocus margin="dense" id="description" label="description" fullWidth value={description}
                       onChange={(e) => setDescription(e.target.value)} />
            <TextField autoFocus margin="dense" id="price" label="quantity" fullWidth value={quantity}
                       InputProps={{inputComponent: NumberFormatCustom}}
                       onChange={(e) => setQuantity(e.target.value)}/>
            <TextField autoFocus margin="dense" id="price" label="price" fullWidth InputProps={{
            startAdornment: <InputAdornment position="start">???</InputAdornment>, inputComponent: NumberFormatCustom,
          }}           onChange={(e) => setPrice(e.target.value)}
            value={price}/>
            <TextField autoFocus margin="dense" id="name" label="categories" fullWidth value={categories}
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
