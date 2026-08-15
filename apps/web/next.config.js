/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@datumbim/ui', '@datumbim/core', '@datumbim/database', '@datumbim/bim-engine', '@datumbim/sdk-manager', '@datumbim/format-engine', '@datumbim/viewer', '@datumbim/shared'],
}

module.exports = nextConfig
