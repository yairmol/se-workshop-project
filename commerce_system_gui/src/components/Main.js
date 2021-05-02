import {Input} from "@material-ui/core";
import {useState} from "react";
import Button from "@material-ui/core/Button";

export const Main = () => {
  const [query, setQuery] = useState("");
  const onSearch = () => {

  }

  return (
      <div>
        <Input value={query} onChange={(e) => setQuery(...)}/>
        <Button onSubmit={}/>
      </div>
  );
};