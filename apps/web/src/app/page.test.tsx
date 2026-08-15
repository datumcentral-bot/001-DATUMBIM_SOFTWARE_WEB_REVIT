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

  it('renders task indicator for TASK 006F', async () => {
    render(<Home />)
    expect(screen.getByText('TASK 006F — Real Frontend')).toBeDefined()
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

  it('renders top bar with file menu', async () => {
    render(<Home />)
    expect(screen.getByText('File')).toBeDefined()
  })

  it('renders viewport controls', async () => {
    render(<Home />)
    expect(screen.getByText('Zoom In')).toBeDefined()
    expect(screen.getByText('Zoom Out')).toBeDefined()
    expect(screen.getByText('Fit')).toBeDefined()
  })
})
