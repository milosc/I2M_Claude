/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    optimizePackageImports: ['@adobe/react-spectrum']
  }
}

module.exports = nextConfig
