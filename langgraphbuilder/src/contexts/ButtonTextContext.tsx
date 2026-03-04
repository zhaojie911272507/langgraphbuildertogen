import React, { createContext, useState, useContext } from 'react'

type ButtonTextContextType = {
  buttonTexts: { [key: string]: string }
  updateButtonText: (id: string, text: string) => void
}

const ButtonTextContext = createContext<ButtonTextContextType | undefined>(undefined)

export const ButtonTextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [buttonTexts, setButtonTexts] = useState<{ [key: string]: string }>({})

  const updateButtonText = (id: string, text: string) => {
    setButtonTexts((prev) => ({ ...prev, [id]: text }))
  }

  return <ButtonTextContext.Provider value={{ buttonTexts, updateButtonText }}>{children}</ButtonTextContext.Provider>
}

export const useButtonText = () => {
  const context = useContext(ButtonTextContext)
  if (context === undefined) {
    throw new Error('useButtonText must be used within a ButtonTextProvider')
  }
  return context
}
