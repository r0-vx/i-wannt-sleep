import { Plus } from "lucide-react";
import Link from "next/link";
import { InvestigationList } from "@/components/investigation-list";
import { MotionPage } from "@/components/motion-primitives";
import { PageHeading } from "@/components/page-heading";

export default function InvestigationsPage(){return <MotionPage className="page-shell"><PageHeading eyebrow="Private history" title="Your Investigations" description="Search, filter, open, or delete records associated with this browser’s guest session." actions={<Link href="/investigations/new" className="button-primary"><Plus aria-hidden="true" size={17}/>New Investigation</Link>}/><div className="mt-8"><InvestigationList/></div></MotionPage>;}
