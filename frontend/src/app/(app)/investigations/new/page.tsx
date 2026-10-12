"use client";

import { ArrowRight, FileAudio, FileImage, FileText, Info, Link2, LockKeyhole, MessageSquareText, Scan, UploadCloud, X } from "lucide-react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import { MotionPage } from "@/components/motion-primitives";
import { PageHeading } from "@/components/page-heading";
import { ApiError, createAndVerify } from "@/lib/api";

const tabs = [
  { id: "text", label: "Text", icon: MessageSquareText, live: true },
  { id: "screenshot", label: "Screenshot", icon: Scan, live: false },
  { id: "image", label: "Image", icon: FileImage, live: false },
  { id: "voice", label: "Voice", icon: FileAudio, live: false },
  { id: "pdf", label: "PDF", icon: FileText, live: false },
  { id: "url", label: "URL", icon: Link2, live: false },
] as const;
type InputMode = typeof tabs[number]["id"];

export default function NewInvestigationPage() {
  const router = useRouter();
  const [mode, setMode] = useState<InputMode>("text");
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("auto");
  const [caption, setCaption] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const fileUrl = useMemo(() => file ? URL.createObjectURL(file) : "", [file]);
  useEffect(() => () => { if (fileUrl) URL.revokeObjectURL(fileUrl); }, [fileUrl]);
  const remaining = 30_000 - text.length;
  const validUrl = useMemo(() => { try { const parsed = new URL(url); return parsed.protocol === "http:" || parsed.protocol === "https:"; } catch { return false; } }, [url]);

  function switchMode(next: InputMode) { setMode(next); setFile(null); setUrl(""); setError(""); }
  function chooseFile(next: File | undefined) {
    if (!next) return;
    if (next.size > 15_000_000) { setError("Files must be 15 MB or smaller."); return; }
    const valid = mode === "pdf" ? next.type === "application/pdf" : mode === "voice" ? next.type.startsWith("audio/") : next.type.startsWith("image/");
    if (!valid) { setError(`Choose a valid ${mode === "pdf" ? "PDF" : mode === "voice" ? "audio" : "image"} file.`); return; }
    setError(""); setFile(next);
  }
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (mode !== "text") return;
    setError(""); setSubmitting(true);
    try { const investigation = await createAndVerify({ text, language, caption: caption || undefined }); router.push(`/investigations/${investigation.id}/processing`); }
    catch (caught) { setError(caught instanceof ApiError ? caught.message : "Could not start the investigation."); setSubmitting(false); }
  }

  return <MotionPage className="page-shell"><PageHeading eyebrow="New investigation" title="What would you like to verify?" description="Paste a message or inspect suspicious content. ForwardCheck will only start workflows supported by the current backend."/><div className="mt-9 overflow-x-auto pb-2"><div role="tablist" aria-label="Investigation input format" className="inline-flex min-w-full gap-1 rounded-2xl border border-[var(--border)] bg-white p-1.5 shadow-sm sm:min-w-0">{tabs.map(({id,label,icon:Icon,live})=><button key={id} id={`tab-${id}`} role="tab" aria-selected={mode===id} aria-controls={`panel-${id}`} type="button" onClick={()=>switchMode(id)} className={`relative flex min-h-11 flex-1 items-center justify-center gap-2 whitespace-nowrap rounded-xl px-3 text-sm font-semibold transition-all ${mode===id ? "bg-[var(--indigo)] text-white shadow-sm" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"}`}><Icon aria-hidden="true" size={17}/>{label}{live ? <span className={`size-1.5 rounded-full ${mode===id ? "bg-emerald-300" : "bg-emerald-500"}`} aria-label="Available now"/> : null}</button>)}</div></div>
  <form onSubmit={submit} className="mt-6 grid gap-5"><section id={`panel-${mode}`} role="tabpanel" aria-labelledby={`tab-${mode}`} className="premium-card p-5 sm:p-7">{mode === "text" ? <TextPanel text={text} setText={setText} remaining={remaining} language={language} setLanguage={setLanguage} caption={caption} setCaption={setCaption}/> : mode === "url" ? <UrlPanel url={url} setUrl={setUrl} valid={validUrl}/> : <FilePanel mode={mode} file={file} fileUrl={fileUrl} dragging={dragging} setDragging={setDragging} chooseFile={chooseFile} clear={()=>setFile(null)}/>}</section>
  {mode !== "text" ? <div className="rounded-[18px] border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-900"><strong className="block">Preview is local; processing is not connected yet.</strong>The control above validates and previews your selected content without claiming an upload succeeded. {mode === "url" ? "Direct URL extraction" : mode === "voice" ? "Audio transcription" : mode === "pdf" ? "PDF extraction" : "OCR and image-context analysis"} remains a backend roadmap item.</div> : null}
  <div className="grid gap-4 rounded-[18px] border border-[var(--border)] bg-white p-4 text-sm leading-6 text-[var(--text-muted)] md:grid-cols-2"><p className="flex gap-3"><LockKeyhole aria-hidden="true" className="mt-1 shrink-0 text-[var(--teal)]" size={18}/>Guest investigations are scoped to a random session ID stored in this browser.</p><p className="flex gap-3"><Info aria-hidden="true" className="mt-1 shrink-0 text-[var(--indigo)]" size={18}/>Submitted text may be sent to configured search and AI providers. Do not include private personal information.</p></div>
  {error ? <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">{error}</div> : null}<div className="flex items-center justify-between gap-4"><p className="text-xs text-[var(--text-muted)]">Only the text workflow currently reaches the live verification backend.</p><button type="submit" disabled={mode!=="text" || submitting || text.trim().length<20} className="button-primary min-h-12 px-5">{mode!=="text" ? "Processor not connected" : submitting ? "Starting investigation…" : "Start Investigation"}<ArrowRight aria-hidden="true" size={18}/></button></div></form></MotionPage>;
}

function TextPanel({text,setText,remaining,language,setLanguage,caption,setCaption}:{text:string;setText:(v:string)=>void;remaining:number;language:string;setLanguage:(v:string)=>void;caption:string;setCaption:(v:string)=>void}) {
  return <><div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-xl bg-[var(--indigo-soft)] text-[var(--indigo)]"><MessageSquareText aria-hidden="true" size={21}/></span><div><h2 className="font-bold">Pasted message</h2><p className="text-sm text-[var(--text-muted)]">The complete live investigation workflow.</p></div></div><label htmlFor="forward-text" className="mt-7 block text-sm font-semibold">Forwarded content</label><textarea id="forward-text" required minLength={20} maxLength={30000} value={text} onChange={(event)=>setText(event.target.value)} className="input-control mt-2 min-h-[280px] resize-y p-4 leading-7" placeholder="Paste the full message here, including dates, numbers, links, and forwarding instructions…" aria-describedby="text-help"/><div id="text-help" className="mt-2 flex justify-between gap-4 text-xs text-[var(--text-muted)]"><span>Minimum 20 characters</span><span className={`font-metric ${remaining<500 ? "text-amber-700" : ""}`}>{remaining.toLocaleString()} left</span></div><div className="mt-6 grid gap-5 md:grid-cols-2"><label className="text-sm font-semibold" htmlFor="language">Explanation language<select id="language" value={language} onChange={(event)=>setLanguage(event.target.value)} className="input-control mt-2 font-normal"><option value="auto">Detect automatically</option><option value="en">English</option><option value="hi">Hindi</option><option value="mr">Marathi</option></select></label><label className="text-sm font-semibold" htmlFor="caption">Context <span className="font-normal text-[var(--text-muted)]">(optional)</span><input id="caption" maxLength={1000} value={caption} onChange={(event)=>setCaption(event.target.value)} className="input-control mt-2 font-normal" placeholder="Where and when did you receive it?"/></label></div></>;
}

function UrlPanel({url,setUrl,valid}:{url:string;setUrl:(v:string)=>void;valid:boolean}) {
  return <div><div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-xl bg-[var(--indigo-soft)] text-[var(--indigo)]"><Link2 aria-hidden="true" size={21}/></span><div><h2 className="font-bold">Public webpage URL</h2><p className="text-sm text-[var(--text-muted)]">Validation works locally; retrieval is not wired to submission.</p></div></div><label htmlFor="source-url" className="mt-7 block text-sm font-semibold">Article or public page</label><input id="source-url" type="url" value={url} onChange={(event)=>setUrl(event.target.value)} className="input-control mt-2" placeholder="https://example.org/article"/><div aria-live="polite" className={`mt-4 rounded-xl border p-4 text-sm ${!url ? "border-[var(--border)] text-[var(--text-muted)]" : valid ? "border-emerald-200 bg-emerald-50 text-emerald-800" : "border-rose-200 bg-rose-50 text-rose-800"}`}>{!url ? "Enter a public HTTP or HTTPS URL." : valid ? `Valid public URL · ${new URL(url).hostname}` : "Enter a complete HTTP or HTTPS URL."}</div></div>;
}

function FilePanel({mode,file,fileUrl,dragging,setDragging,chooseFile,clear}:{mode:Exclude<InputMode,"text"|"url">;file:File|null;fileUrl:string;dragging:boolean;setDragging:(v:boolean)=>void;chooseFile:(f:File|undefined)=>void;clear:()=>void}) {
  const accept = mode === "pdf" ? "application/pdf" : mode === "voice" ? "audio/*" : "image/*";
  const names = { screenshot: "screenshot", image: "image", voice: "voice note", pdf: "PDF document" };
  return <div><div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-xl bg-[var(--indigo-soft)] text-[var(--indigo)]"><UploadCloud aria-hidden="true" size={21}/></span><div><h2 className="font-bold capitalize">{names[mode]}</h2><p className="text-sm text-[var(--text-muted)]">Choose a file up to 15 MB for a real local preview.</p></div></div>{file ? <div className="mt-7 overflow-hidden rounded-[18px] border border-[var(--border)] bg-slate-50"><div className="flex items-center justify-between gap-4 border-b border-[var(--border)] bg-white p-4"><div className="min-w-0"><p className="truncate text-sm font-bold">{file.name}</p><p className="font-metric mt-1 text-xs text-[var(--text-muted)]">{(file.size/1024/1024).toFixed(2)} MB · {file.type||"unknown type"}</p></div><button type="button" onClick={clear} aria-label="Remove selected file" className="grid size-10 place-items-center rounded-xl border border-[var(--border)] text-slate-600 hover:bg-rose-50 hover:text-rose-700"><X aria-hidden="true" size={18}/></button></div>{mode === "voice" ? <audio className="m-4 w-[calc(100%-2rem)]" controls src={fileUrl}>Your browser does not support audio playback.</audio> : mode === "pdf" ? <div className="grid min-h-48 place-items-center p-8 text-center"><FileText aria-hidden="true" className="text-[var(--indigo)]" size={40}/><p className="mt-3 text-sm text-[var(--text-muted)]">PDF selected and validated. Page extraction is not connected.</p></div> : <div className="grid max-h-[420px] place-items-center overflow-hidden p-4"><Image unoptimized src={fileUrl} alt={`Preview of ${file.name}`} width={1000} height={700} className="max-h-[380px] max-w-full rounded-xl object-contain"/></div>}</div> : <label onDragEnter={(event)=>{event.preventDefault();setDragging(true)}} onDragOver={(event)=>event.preventDefault()} onDragLeave={()=>setDragging(false)} onDrop={(event)=>{event.preventDefault();setDragging(false);chooseFile(event.dataTransfer.files[0])}} className={`relative mt-7 grid min-h-64 cursor-pointer place-items-center rounded-[20px] border-2 border-dashed p-8 text-center transition-all ${dragging ? "border-[var(--indigo)] bg-[var(--indigo-soft)]" : "border-slate-300 bg-slate-50 hover:border-indigo-300 hover:bg-indigo-50/40"}`}><input type="file" accept={accept} aria-label={`Choose ${names[mode]} file`} className="absolute inset-0 z-10 cursor-pointer opacity-0" onChange={(event)=>chooseFile(event.target.files?.[0])}/><span><UploadCloud aria-hidden="true" className="mx-auto text-[var(--indigo)]" size={32}/><strong className="mt-4 block">Drop your {names[mode]} here</strong><span className="mt-2 block text-sm text-[var(--text-muted)]">or choose a file from this device</span></span></label>}</div>;
}
