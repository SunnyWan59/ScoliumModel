"use client";

import { usePathname } from "next/navigation";
import { FC } from "react";

interface DynamicPathDisplayProps {
  className?: string;
}

/**
 * Component that displays the dynamic path segment from the URL
 */
export const DynamicPathDisplay: FC<DynamicPathDisplayProps> = ({ className = "" }) => {
  const pathname = usePathname();
  
  // Extract the dynamic path segment (assuming it's the last part of the URL)
  const pathSegments = pathname.split("/").filter(Boolean);
  const dynamicPath = pathSegments.length > 0 ? pathSegments[pathSegments.length - 1] : "";
  
  return ("Hello");
};
