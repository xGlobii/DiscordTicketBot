import { AppLayout } from "./components/AppLayout"
import { AuthProvider } from "./components/AuthContext"
import { Callback } from "./views/Callback"
import { Commands } from "./views/Commands"
import { Dashboard } from "./views/Dashboard"
import { Tickets } from './views/Tickets'
import { MainPage } from './views/MainPage'
import { BrowserRouter, Route, Routes } from "react-router-dom"

function App() {
  return (
    <>
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route index element={<MainPage />} />
          <Route path="callback" element={<Callback />} />
          <Route path="/" element={<AppLayout/>}>
            <Route path="dashboard" element={<Dashboard />}/>
            <Route path="commands" element={<Commands />}/>
            <Route path="tickets" element={<Tickets />}/>
          </Route>
          <Route path="*" element={<h2>Not found</h2>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
    </>
  )
}

export default App
