 import React, { useState, useEffect } from "react";
 import {
   LayoutDashboard,
   ShieldCheck,
   UserPlus,
   Users,
   FileText,
   BarChart3,
 } from "lucide-react";
 
 const NAV = [
   { key: "main", label: "Main", icon: LayoutDashboard },
   { key: "check", label: "Check ads", icon: ShieldCheck },
   { key: "new-client", label: "New Client", icon: UserPlus },
   { key: "client", label: "Client", icon: Users },
   { key: "ord", label: "ORD", icon: FileText },
   { key: "stat", label: "Statistic", icon: BarChart3 },
 ];
 
 function Sidebar({ active, onSelect }) {
   return (
     <aside className="flex flex-col h-screen w-[15rem] border-r-2 border-gray-700 bg-white dark:bg-gray-900 dark:border-gray-700">
       <div className="flex flex-col w-full h-full">
-        {NAV.map(({ key, label, icon: Icon }, idx) => {
+        {NAV.map(({ key, label, icon }, idx) => {
           const isActive = active === key;
           return (
             <button
               key={key}
               onClick={() => onSelect(key)}
               className={["w-full flex-1 select-none", "flex flex-col items-center justify-center", "px-6", "gap-4", "text-6xl font-extrabold tracking-tight", "bg-white dark:bg-gray-900", "text-gray-900 dark:text-gray-100", "transition-colors duration-150", idx !== 0 ? "border-t-2 border-gray-300 dark:border-gray-700" : "", isActive ? "ring-2 ring-gray-800 dark:ring-gray-200" : "hover:bg-gray-100 dark:hover:bg-gray-800"].join(" ")}
             >
-              <Icon className="h-20 w-20" />
+              {React.createElement(icon, { className: "h-20 w-20" })}
               <span className="text-center leading-none">{label}</span>
             </button>
           );
         })}
       </div>
     </aside>
   );
 }
 
 function NewClientPage() {
   const [executors, setExecutors] = useState([]);
   const [loadingExec, setLoadingExec] = useState(false);
   const [errorExec, setErrorExec] = useState("");
   const [selectedExecutor, setSelectedExecutor] = useState("");
 
   const [contractTypes, setContractTypes] = useState([]);
   const [loadingCT, setLoadingCT] = useState(false);
   const [errorCT, setErrorCT] = useState("");
   const [selectedCT, setSelectedCT] = useState("");
 
   const [date, setDate] = useState("");
   const [number, setNumber] = useState("");
 
   useEffect(() => {
     fetch("/api/executors").then(res => res.json()).then(setExecutors).catch(e => setErrorExec(e.message)).finally(() => setLoadingExec(false));
     fetch("/api/contract-types").then(res => res.json()).then(setContractTypes).catch(e => setErrorCT(e.message)).finally(() => setLoadingCT(false));
   }, []);
 
   return (
     <div className="space-y-10">
       <h1 className="text-4xl font-bold">New Client</h1>
       <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
         <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
-          <h2 className="text-2xl font-semibold mb-4">3. Дата и номер</h2>
-          <label className="block mb-2 font-medium">Дата</label>
-          <input type="text" value={date} onChange={(e) => setDate(e.target.value)} placeholder="01.01.1990" className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3 mb-4" />
-          <label className="block mb-2 font-medium">Номер</label>
-          <input type="text" value={number} onChange={(e) => setNumber(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
+          <h2 className="text-2xl font-semibold mb-4">1. Выбрать исполнителя</h2>
+          <select value={selectedExecutor} onChange={(e) => setSelectedExecutor(e.target.value)} disabled={loadingExec} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-4">
+            <option value="">Выберите исполнителя</option>
+            {executors.map(ex => <option key={ex.id} value={ex.id}>{ex.name_executor}</option>)}
+          </select>
+          {errorExec && <p className="text-red-500">{errorExec}</p>}
         </section>
         <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
           <h2 className="text-2xl font-semibold mb-4">2. Тип договора</h2>
           <select value={selectedCT} onChange={(e) => setSelectedCT(e.target.value)} disabled={loadingCT} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-4">
             <option value="">Выберите тип договора</option>
             {contractTypes.map(ct => <option key={ct.id} value={ct.id}>{ct.contract_type_name}</option>)}
           </select>
           {errorCT && <p className="text-red-500">{errorCT}</p>}
         </section>
         <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
-          <h2 className="text-2xl font-semibold mb-4">1. Выбрать исполнителя</h2>
-          <select value={selectedExecutor} onChange={(e) => setSelectedExecutor(e.target.value)} disabled={loadingExec} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-4">
-            <option value="">Выберите исполнителя</option>
-            {executors.map(ex => <option key={ex.id} value={ex.id}>{ex.name_executor}</option>)}
-          </select>
-          {errorExec && <p className="text-red-500">{errorExec}</p>}
+          <h2 className="text-2xl font-semibold mb-4">3. Дата и номер</h2>
+          <label className="block mb-2 font-medium">Дата</label>
+          <input type="text" value={date} onChange={(e) => setDate(e.target.value)} placeholder="01.01.1990" className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3 mb-4" />
+          <label className="block mb-2 font-medium">Номер</label>
+          <input type="text" value={number} onChange={(e) => setNumber(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
         </section>
       </div>
     </div>
   );
 }
 
 export default function CRMMainLayout() {
   const [active, setActive] = useState("main");
   return (
     <div className="flex h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
       <Sidebar active={active} onSelect={setActive} />
       <main className="flex-1 p-12 overflow-y-auto">
         {active === "main" && <div><h1 className="text-5xl font-bold mb-12">Главная</h1><p className="text-xl">Это главная страница CRM. Здесь будет строгий UI и основные данные.</p></div>}
         {active === "new-client" && <NewClientPage />}
         {active !== "main" && active !== "new-client" && <div><h1 className="text-5xl font-bold mb-12">{NAV.find(n => n.key === active)?.label}</h1><p className="text-xl">Содержимое страницы {active} появится здесь.</p></div>}
       </main>
     </div>
   );
 }
 

        
