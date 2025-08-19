 import React, { useState, useEffect } from "react";

export default function NewClientPage() {
  const [executors, setExecutors] = useState([]);
  const [contracts, setContracts] = useState([]);
  const [clientTypes, setClientTypes] = useState([]);

  const [selectedExecutor, setSelectedExecutor] = useState("");
  const [selectedContract, setSelectedContract] = useState("");
  const [date, setDate] = useState("");
  const [number, setNumber] = useState("");

  const [typeClient, setTypeClient] = useState("");
  const [inn, setInn] = useState("");
  const [ogrn, setOgrn] = useState("");
  const [kpp, setKpp] = useState("");
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [bank, setBank] = useState("");
  const [bik, setBik] = useState("");
  const [cor, setCor] = useState("");
  const [acc, setAcc] = useState("");
  const [tel, setTel] = useState("");
  const [mail, setMail] = useState("");
  const [mess, setMess] = useState("");
  const [contact, setContact] = useState("");
  const [saving, setSaving] = useState(false);
  const [errorSave, setErrorSave] = useState("");

  useEffect(() => {
    fetch("/api/executors").then(r => r.json()).then(setExecutors);
    fetch("/api/sample-contracts").then(r => r.json()).then(setContracts);
    fetch("/api/client-types").then(r => r.json()).then(setClientTypes);
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setErrorSave("");
    try {
      const resp = await fetch("/api/clients", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type_client: Number(typeClient),
          inn_client: inn,
          ogrn_client: ogrn,
          kpp_client: kpp || null,
          name_client: name,
          adress_client: address,
          bank_client: bank,
          bik_bank_client: bik,
          acc_bank_client: acc,
          cor_bank_client: cor,
          tel_client: tel,
          mail_client: mail,
          mess_client: mess,
          contact_name_client: contact,
        }),
      });
      if (!resp.ok) throw new Error("Ошибка сохранения");
    } catch (e) {
      setErrorSave(e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-10">
      <h1 className="text-4xl font-bold">New Client</h1>
      <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
        <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
          <h2 className="text-2xl font-semibold mb-4">1. Выбрать исполнителя</h2>
          <select value={selectedExecutor} onChange={(e) => setSelectedExecutor(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-4">
            <option value="">Выберите исполнителя</option>
            {executors.map(ex => (
              <option key={ex.id_executor || ex.id} value={ex.id_executor || ex.id}>{ex.name_executor}</option>
            ))}
          </select>
          <button disabled className="mt-4 w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3 opacity-50">Создать нового</button>
        </section>
        <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
          <h2 className="text-2xl font-semibold mb-4">2. Тип договора</h2>
          <select value={selectedContract} onChange={(e) => setSelectedContract(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-4">
            <option value="">Выберите тип договора</option>
            {contracts.map(ct => (
              <option key={ct.id_sample_contract} value={ct.id_sample_contract}>{ct.name_sample_contract}</option>
            ))}
          </select>
          <button disabled className="mt-4 w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3 opacity-50">Создать новый</button>
        </section>
        <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
          <h2 className="text-2xl font-semibold mb-4">3. Дата и номер</h2>
          <label className="block mb-2 font-medium">Дата</label>
          <input type="text" value={date} onChange={(e) => setDate(e.target.value)} placeholder="01.01.1990" className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3 mb-4" />
          <label className="block mb-2 font-medium">Номер</label>
          <input type="text" value={number} onChange={(e) => setNumber(e.target.value)} maxLength={15} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
        </section>
      </div>
      <section className="rounded-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 p-6">
        <h2 className="text-2xl font-semibold mb-4">Данные заказчика</h2>
        <button disabled className="mb-6 rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3 opacity-50">Загрузить карточку предприятия</button>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block mb-2 font-medium">Форма</label>
            <select value={typeClient} onChange={(e) => setTypeClient(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3">
              <option value="">Выберите форму</option>
              {clientTypes.map(t => (
                <option key={t.id_type_client} value={t.id_type_client}>{t.id_type_long}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block mb-2 font-medium">ИНН</label>
            <input type="text" value={inn} onChange={(e) => setInn(e.target.value)} maxLength={12} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">ОГРН</label>
            <input type="text" value={ogrn} onChange={(e) => setOgrn(e.target.value)} maxLength={15} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">КПП</label>
            <input type="text" value={kpp} onChange={(e) => setKpp(e.target.value)} maxLength={9} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-2 font-medium">Наименование компании</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-2 font-medium">Адрес</label>
            <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-2 font-medium">Банк</label>
            <input type="text" value={bank} onChange={(e) => setBank(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">БИК</label>
            <input type="text" value={bik} onChange={(e) => setBik(e.target.value)} maxLength={9} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">к/с</label>
            <input type="text" value={cor} onChange={(e) => setCor(e.target.value)} maxLength={20} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">р/с</label>
            <input type="text" value={acc} onChange={(e) => setAcc(e.target.value)} maxLength={20} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">Тел.</label>
            <input type="text" value={tel} onChange={(e) => setTel(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">Почта</label>
            <input type="text" value={mail} onChange={(e) => setMail(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">Мессенджер</label>
            <input type="text" value={mess} onChange={(e) => setMess(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
          <div>
            <label className="block mb-2 font-medium">Контактное лицо</label>
            <input type="text" value={contact} onChange={(e) => setContact(e.target.value)} className="w-full rounded-xl border-2 border-gray-400 dark:border-gray-600 px-4 py-3" />
          </div>
        </div>
        {errorSave && <p className="text-red-500 mt-4">{errorSave}</p>}
        <button onClick={handleSave} disabled={saving} className="mt-6 w-full rounded-xl bg-blue-600 text-white px-4 py-3 disabled:opacity-50">Сохранить</button>
      </section>
    </div>
  );
}
