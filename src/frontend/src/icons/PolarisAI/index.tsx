import React, { forwardRef } from "react";
import SvgPolarisAILogo from "./PolarisAILogo";

export const PolarisAIIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgPolarisAILogo ref={ref} {...props} />;
});
