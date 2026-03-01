export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Dreamsoft Pro 2.0</h1>
      <p className="text-xl text-slate-500 mb-8">System zmodernizowany przez RAE-Feniks</p>
      
      <div className="flex space-x-4">
        <a href="/kalkulator" className="px-6 py-3 bg-blue-600 text-white rounded-md shadow hover:bg-blue-700 transition">Idź do Kalkulatora</a>
        <a href="/koszyk" className="px-6 py-3 bg-green-600 text-white rounded-md shadow hover:bg-green-700 transition">Przejdź do Koszyka</a>
      </div>
    </div>
  );
}