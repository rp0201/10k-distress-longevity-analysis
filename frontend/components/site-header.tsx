"use client"

import Image from "next/image"
import Link from "next/link"
import { Menu } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetTitle,
} from "@/components/ui/sheet"
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import { cn } from "@/lib/utils"

export function SiteHeader() {
  return (
    <header className="flex justify-between items-center w-full">
      <Link href="/" className="flex items-center gap-2">
        <Image
          src="/10k_analyzer.svg"
          alt="10K Analyzer"
          width={123}
          height={20}
          priority
        />
      </Link>
      <div className="hidden md:flex absolute left-1/2 transform -translate-x-1/2">
        <NavigationMenu>
          <NavigationMenuList className="gap-2">
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link href="/" className={cn(navigationMenuTriggerStyle(), "bg-transparent text-gray-300 hover:text-white hover:bg-[#1A1816] px-6")}>
                  Home
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link href="/limitations" className={cn(navigationMenuTriggerStyle(), "bg-transparent text-gray-300 hover:text-white hover:bg-[#1A1816] px-6")}>
                  Limitations
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
      
      <div className="hidden md:flex">
        <Button 
          variant="default" 
          size="sm" 
          className="bg-[#1A70A5] hover:bg-[#155A8A] text-white gap-2"
          asChild
        >
          <Link 
            href="https://github.com/rp0201/10k-distress-longevity-analysis"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image 
              src="/github.svg" 
              alt="GitHub" 
              width={16} 
              height={16}
            />
            GitHub
          </Link>
        </Button>
      </div>

      {/* Mobile Menu */}
      <Sheet>
        <SheetTrigger asChild className="md:hidden">
          <Button variant="ghost" size="icon" className="text-white hover:bg-[#1A1816]">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="top" className="bg-[#12100E] border-[#31302F]">
          <SheetTitle className="sr-only">Navigation Menu</SheetTitle>
          <nav className="flex flex-col gap-2 mt-6 mb-6 items-center">
            <Link 
              href="/" 
              className="w-full max-w-xs text-center py-2 px-6 rounded-md bg-transparent text-gray-300 hover:text-white hover:bg-[#1A1816] transition-colors font-medium"
            >
              Home
            </Link>
            <Link 
              href="/limitations" 
              className="w-full max-w-xs text-center py-2 px-6 rounded-md bg-transparent text-gray-300 hover:text-white hover:bg-[#1A1816] transition-colors font-medium"
            >
              Limitations
            </Link>
            <Button 
              variant="default" 
              size="default" 
              className="bg-[#1A70A5] hover:bg-[#155A8A] text-white gap-2 mt-2 w-full max-w-xs"
              asChild
            >
              <Link 
                href="https://github.com/rp0201/10k-distress-longevity-analysis"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Image 
                  src="/github.svg" 
                  alt="GitHub" 
                  width={20} 
                  height={20}
                />
                View on GitHub
              </Link>
            </Button>
          </nav>
        </SheetContent>
      </Sheet>
    </header>
  )
}