/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',
    reactStrictMode: true,
    experimental: {
        serverActions: {
            bodySizeLimit: '3mb',
        }
    }
}

module.exports = nextConfig
