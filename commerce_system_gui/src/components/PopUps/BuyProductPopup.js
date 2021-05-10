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
import Typography from "@material-ui/core/Typography";

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


export default function BuyProductPopup({product, add_to_cart_func}) {
  const [open, setOpen] = useState(true)

  const get_categories = () => {
    let cat_str = product.categories[0]
    for (let i =1; i<product.categories.length; i++) {
      cat_str += ', ' + product.categories[i]
    }
    return cat_str
  }

  const handleClose = () => {
    setOpen(false)
  }

  const done = () => {
    /*
    CALL FOR BUY
     */
    add_to_cart_func(product.product_id)
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
          {product.product_name}
        </DialogTitle>
        <DialogContent>
          <Typography>{product.description}</Typography>
          <Typography>{product.quantity} available</Typography>
          <Typography>price is {product.price}ils</Typography>
          <Typography>{product.description}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={done} color="primary">
            Add To Cart
          </Button>
          <Button onClick={handleClose} color="primary" autoFocus>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
