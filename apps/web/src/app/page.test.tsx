import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import Home from '../app/page'

describe('Home Page', () => {
  it('renders DATUMBIM application shell', async () => {
    render(<Home />)
    const elements = screen.getAllByText('DATUMBIM')
    expect(elements.length).toBeGreaterThanOrEqual(1)
  })

  it('renders task indicator', async () => {
    render(<Home />)
    expect(screen.getByText('TASK 002 — Application Shell')).toBeDefined()
  })

  it('renders ribbon tabs', async () => {
    render(<Home />)
    expect(screen.getByText('Architecture')).toBeDefined()
    expect(screen.getByText('Structure')).toBeDefined()
    expect(screen.getByText('MEP')).toBeDefined()
    const datumbimElements = screen.getAllByText('DATUMBIM')
    expect(datumbimElements.length).toBeGreaterThanOrEqual(1)
  })

  it('renders project browser', async () => {
    render(<Home />)
    expect(screen.getByText('Project Browser')).toBeDefined()
  })

  it('renders properties panel', async () => {
    render(<Home />)
    expect(screen.getByText('Properties')).toBeDefined()
  })

  it('renders status bar', async () => {
    render(<Home />)
    expect(screen.getByText('READY')).toBeDefined()
  })
})
