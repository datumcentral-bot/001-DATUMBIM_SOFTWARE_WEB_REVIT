'use client'

import React from 'react'
import { useShellStore } from '@/store/shellStore'

const TYPE_COLORS = {
  info: 'bg-blue-500/20 border-blue-500/40 text-blue-200',
  success: 'bg-green-500/20 border-green-500/40 text-green-200',
  warning: 'bg-yellow-500/20 border-yellow-500/40 text-yellow-200',
  error: 'bg-red-500/20 border-red-500/40 text-red-200',
}

export default function Notifications() {
  const { notifications, removeNotification } = useShellStore()

  if (notifications.length === 0) return null

  return (
    <div className="fixed top-14 right-4 z-50 flex flex-col gap-2 max-w-sm">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`border rounded px-3 py-2 text-xs shadow-lg flex items-start gap-2 ${
            TYPE_COLORS[notification.type]
          }`}
        >
          <span className="flex-1">{notification.message}</span>
          <button
            onClick={() => removeNotification(notification.id)}
            className="text-current opacity-60 hover:opacity-100"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  )
}
