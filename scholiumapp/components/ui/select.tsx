"use client";

import * as React from "react"
import * as SelectPrimitive from "@radix-ui/react-select"
import { useStyleContext } from "../../lib/citation-context";
import { Select } from "radix-ui";
import classnames from "classnames";
import {
	CheckIcon,
	ChevronDownIcon,
	ChevronUpIcon,
} from "@radix-ui/react-icons";
import "./select-style.css";



const SelectCitation= () => {
    const { style, setStyle } = useStyleContext();
    return(
        <Select.Root value={style} onValueChange={setStyle}>
            <Select.Trigger className="SelectTrigger" aria-label="Food">
                <Select.Value placeholder="Citation Style" />
                <Select.Icon className="SelectIcon">
                    <ChevronDownIcon />
                </Select.Icon>
            </Select.Trigger>
            <Select.Portal>
                <Select.Content className="SelectContent">
                    <Select.ScrollUpButton className="SelectScrollButton">
                        <ChevronUpIcon />
                    </Select.ScrollUpButton>
                    <Select.Viewport className="SelectViewport">
                        <Select.Group style={{ backgroundColor: 'rgba(255, 255, 255, 0.95)' }}>
                            <SelectItem value="APA">APA</SelectItem>
                            <SelectItem value="MLA">MLA</SelectItem>
                            <SelectItem value="Chicago">Chicago</SelectItem>
                            <SelectItem value="Harvard">Harvard</SelectItem>
                            <SelectItem value="Vancouver">Vancouver</SelectItem>
                        </Select.Group>
                    </Select.Viewport>
                    <Select.ScrollDownButton className="SelectScrollButton">
                        <ChevronDownIcon />
                    </Select.ScrollDownButton>
                </Select.Content>
            </Select.Portal>
        </Select.Root>
    )
};

const SelectItem = React.forwardRef<
	HTMLDivElement,
	React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ children, className, ...props }, ref) => {
	return (
		<SelectPrimitive.Item
			ref={ref}
			className={classnames("SelectItem", className)}
			{...props}
		>
			<SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
			<SelectPrimitive.ItemIndicator className="SelectItemIndicator">
				<CheckIcon/>
			</SelectPrimitive.ItemIndicator>
		</SelectPrimitive.Item>
	);
});
SelectItem.displayName = "SelectCitation";

export default SelectCitation;
