import { AppLayout } from "./components/AppLayout"
import { Commands } from "./views/Commands"
import { Dashboard } from "./views/Dashboard"
import { BrowserRouter, Route, Routes } from "react-router-dom"

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout/>}>
            <Route index element={<Dashboard />}/>
            <Route path="/dashboard" element={<Dashboard />}/>
            <Route path="/commands" element={<Commands />}/>
          </Route>
          <Route path="*" element={<h2>Not found</h2>} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
