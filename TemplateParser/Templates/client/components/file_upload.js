import React from 'react';
import { styled } from '@mui/material/styles';
import {
  Button,
  Chip
} from '@mui/material'

const Input = styled('input')({
  display: 'none',
});

export default function FileUpload(props) {

  const callBackChange = (e) => {
    const { onChange } = props;
    onChange(e);
  }

  const callBackDelete = (fileName) => {
    const { onDelete } = props;
    onDelete(fileName);
  }

  return (
    <div>
      {/* Upload Button */}
      <label htmlFor="contained-button-file">
        <Input 
          id="contained-button-file"
          accept={props.accept ? props.accept : "*"} 
          multiple={props.multiple} 
          type="file"
          onChange={callBackChange}
        />
        <Button variant="contained" component="span">
          {props.label ? props.label : "Upload File"}
        </Button>
      </label>

      {/* Selected Files Display */}
      { props.variant === "chips" ? 
        <div>
          {props.files && props.files.map((file, i) => (
            <Chip 
              style={{margin: "15px 5px 0px 5px"}}
              key={i}
              label={file.name} 
              variant="outlined" 
              onDelete={props.onDelete && (() => callBackDelete(file.name))}
            />
          ))}
        </div>
      :
        <div style={{marginTop: 5}}>
          {props.files && props.files.map((file, i) => (
            file.name + (i !== props.files.length - 1 ? ", " : "")
          ))}
        </div>
      }
    </div>
  )
}