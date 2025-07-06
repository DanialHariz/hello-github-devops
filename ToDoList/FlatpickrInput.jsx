import React from "react";
import Flatpickr from "react-flatpickr";
import "flatpickr/dist/flatpickr.css";

export default function FlatpickrInput({ value, onChange }) {
  return (
    <Flatpickr
      value={value}
      onChange={(date) => onChange(date[0].toISOString().slice(0, 10))}
      options={{ dateFormat: "Y-m-d" }}
    />
  );
}
