"use client";

import * as React from "react"
import { useStyleContext } from "../../lib/citation-context";
import { Button } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { ChevronDown } from "lucide-react";

const SelectCitation = () => {
    const { style, setStyle } = useStyleContext();
    return (
        <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
                <Button variant="soft">
                    {style || "Citation Style"}
                    <ChevronDown className="h-4 w-4" />
                </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content className="bg-white rounded-md p-1 shadow-lg"> 
                <DropdownMenu.Item onClick={() => setStyle('APA')}>APA</DropdownMenu.Item>
                <DropdownMenu.Item onClick={() => setStyle('MLA')}>MLA</DropdownMenu.Item>
                <DropdownMenu.Item onClick={() => setStyle('Chicago')}>Chicago</DropdownMenu.Item>
                <DropdownMenu.Item onClick={() => setStyle('Harvard')}>Harvard</DropdownMenu.Item>
                <DropdownMenu.Item onClick={() => setStyle('Vancouver')}>Vancouver</DropdownMenu.Item>
            </DropdownMenu.Content>
        </DropdownMenu.Root>
    );
};

export default SelectCitation;