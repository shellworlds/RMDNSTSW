# RMDNSTSW Integration Guide for Zi-US Enterprise Page

This guide provides instructions for integrating the **Quantum Finance Risk Model (QFRM)** into the Zi-US Enterprise page at `https://www.zi-us.com/enterprise`.

## Quick Links

| Resource | URL |
|----------|-----|
| **Live Platform** | `https://shellworlds.github.io/RMDNSTSW/` |
| **GitHub Repository** | `https://github.com/shellworlds/RMDNSTSW` |
| **Platform Page** | `rmdnstsw.html` |
| **Documentation** | `index.html` |

---

## 1. Enterprise Card Component (React/Next.js)

Add this card component to the **Dedicated Commerce Platform** section on `/enterprise`, positioned **after the AEGIRMARN card**:

### JSX/TSX Component

```jsx
{/* RMDNSTSW Card - Add after AEGIRMARN */}
<div className="card">
  <h3>RMDNSTSW</h3>
  <p>
    Quantum Finance Risk Model - Advanced quantum simulation for financial market risk analysis 
    combining 20-qubit quantum circuits with VaR, CVaR, Sharpe ratio, and real-time market data 
    for comprehensive portfolio risk assessment.
  </p>
  <div className="tags">
    <span className="tag">Quantum Computing</span>
    <span className="tag">Risk Analysis</span>
    <span className="tag">Qiskit</span>
    <span className="tag">Finance</span>
  </div>
  <div className="card-links">
    <a href="/rmdnstsw" className="card-link">
      QFRM Platform →
    </a>
    <a 
      href="https://github.com/shellworlds/RMDNSTSW" 
      target="_blank" 
      rel="noopener noreferrer"
      className="card-link"
    >
      GitHub Repo →
    </a>
    <a 
      href="https://shellworlds.github.io/RMDNSTSW/" 
      target="_blank" 
      rel="noopener noreferrer"
      className="card-link"
    >
      Live Demo →
    </a>
  </div>
</div>
```

### HTML Version

```html
<!-- RMDNSTSW Card - Add after AEGIRMARN card in Dedicated Commerce Platform section -->
<div class="card">
  <h3>RMDNSTSW</h3>
  <p>
    Quantum Finance Risk Model - Advanced quantum simulation for financial market risk analysis 
    combining 20-qubit quantum circuits with VaR, CVaR, Sharpe ratio, and real-time market data 
    for comprehensive portfolio risk assessment.
  </p>
  <div class="tags">
    <span class="tag">Quantum Computing</span>
    <span class="tag">Risk Analysis</span>
    <span class="tag">Qiskit</span>
    <span class="tag">Finance</span>
  </div>
  <div class="card-links">
    <a href="/rmdnstsw" class="card-link">QFRM Platform →</a>
    <a href="https://github.com/shellworlds/RMDNSTSW" target="_blank" class="card-link">GitHub Repo →</a>
    <a href="https://shellworlds.github.io/RMDNSTSW/" target="_blank" class="card-link">Live Demo →</a>
  </div>
</div>
```

---

## 2. RMDNSTSW Detail Page Component (Next.js)

Create a new page at `app/rmdnstsw/page.tsx` or `pages/rmdnstsw.tsx`:

```tsx
// app/rmdnstsw/page.tsx (Next.js 13+ App Router)
import Link from 'next/link';

export const metadata = {
  title: 'RMDNSTSW | Zi-US - Quantum Finance Risk Model',
  description: 'Advanced quantum simulation for financial market risk analysis combining quantum computing with traditional finance metrics',
};

export default function RMDNSTSWPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-b border-gray-200 z-50 px-8 py-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <Link href="/" className="text-lg font-normal">Zi-US</Link>
          <Link href="/enterprise" className="text-sm text-gray-500 hover:text-gray-900">
            ← Back to Portfolio
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <header className="pt-32 pb-16 px-8 text-center bg-gradient-to-b from-gray-50 to-white">
        <h1 className="text-5xl font-extralight tracking-widest text-purple-600 mb-6">
          RMDNSTSW
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Quantum Finance Risk Model - Advanced quantum simulation for financial market risk 
          analysis combining 20-qubit quantum circuits with traditional VaR, CVaR, and Sharpe 
          ratio metrics for comprehensive portfolio risk assessment.
        </p>
        <div className="flex justify-center gap-3 mt-8 flex-wrap">
          <span className="px-3 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
            ⚛️ Quantum Computing
          </span>
          <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">VaR/CVaR</span>
          <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">Risk Analysis</span>
          <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">Qiskit</span>
        </div>
      </header>

      {/* Content Cards */}
      <main className="max-w-6xl mx-auto px-8 pb-16">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Live Platform Card */}
          <div className="border border-gray-200 rounded-lg p-8 hover:border-gray-300 transition-colors">
            <h3 className="text-xl font-medium mb-3">Live Platform</h3>
            <p className="text-gray-600 mb-6">
              Access the fully deployed QFRM platform with interactive risk dashboards, 
              quantum circuit visualization, and real-time market data analysis.
            </p>
            <div className="flex gap-3 flex-wrap">
              <a 
                href="https://shellworlds.github.io/RMDNSTSW/" 
                target="_blank"
                className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
              >
                Launch Platform →
              </a>
              <a 
                href="https://shellworlds.github.io/RMDNSTSW/finance_risk_output/finance_risk_report_20251219_235149.html" 
                target="_blank"
                className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded hover:bg-gray-200 transition-colors"
              >
                Interactive Report →
              </a>
            </div>
          </div>

          {/* Source Code Card */}
          <div className="border border-gray-200 rounded-lg p-8 hover:border-gray-300 transition-colors">
            <h3 className="text-xl font-medium mb-3">Source Code</h3>
            <p className="text-gray-600 mb-6">
              Explore the complete source code, documentation, and development resources 
              for the Quantum Finance Risk Model.
            </p>
            <div className="flex gap-3 flex-wrap">
              <a 
                href="https://github.com/shellworlds/RMDNSTSW" 
                target="_blank"
                className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
              >
                GitHub Repository →
              </a>
              <a 
                href="https://github.com/shellworlds/RMDNSTSW/blob/main/qfrm.py" 
                target="_blank"
                className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded hover:bg-gray-200 transition-colors"
              >
                View Source →
              </a>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-12 text-center bg-gray-50 rounded-lg py-12 px-8">
          <h2 className="text-2xl font-normal mb-3">Ready to Explore Quantum Finance?</h2>
          <p className="text-gray-600 mb-6">
            Join us in advancing financial risk analysis through quantum computing.
          </p>
          <Link 
            href="/contact" 
            className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors inline-block"
          >
            Contact Us →
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-6 text-center">
        <a 
          href="https://www.linkedin.com/company/zi-us" 
          target="_blank"
          className="text-gray-500 hover:text-gray-700 text-sm"
        >
          Follow us on LinkedIn
        </a>
      </footer>
    </div>
  );
}
```

---

## 3. Static Files to Host

The following files from `shellworlds/RMDNSTSW` should be accessible:

| File | Description |
|------|-------------|
| `index.html` | Main documentation page |
| `rmdnstsw.html` | Platform landing page |
| `qfrm.py` | Source code |
| `finance_risk_output/` | Output directory with all generated files |

### Option A: GitHub Pages (Recommended)

Enable GitHub Pages on `shellworlds/RMDNSTSW` to serve at:
```
https://shellworlds.github.io/RMDNSTSW/
```

### Option B: Vercel Deployment

Deploy to Vercel from the shellworlds/RMDNSTSW repo.

### Option C: Embed in Zi-US

Copy the following files to the `BorelSigmaInc/my-portfolio-site` repo:
- `public/rmdnstsw/` directory with all QFRM files

---

## 4. Required Links

Update these URLs in the card component based on your deployment:

| Link | Value |
|------|-------|
| Platform Page | `/rmdnstsw` or external URL |
| GitHub Repo | `https://github.com/shellworlds/RMDNSTSW` |
| Live Demo | Deployed URL (GitHub Pages or Vercel) |

---

## 5. Git Integration Commands

To create a branch for this integration:

```bash
# In the BorelSigmaInc/my-portfolio-site repo
git checkout -b feature/rmdnstsw-integration

# Add the RMDNSTSW submodule or copy files
git submodule add https://github.com/shellworlds/RMDNSTSW.git public/rmdnstsw

# Or copy files directly
mkdir -p public/rmdnstsw
cp -r /path/to/RMDNSTSW/* public/rmdnstsw/

# Commit
git add .
git commit -m "Add RMDNSTSW Quantum Finance Risk Model integration

- Add enterprise card for QFRM
- Add /rmdnstsw detail page
- Link to shellworlds/RMDNSTSW repository"

# Push
git push origin feature/rmdnstsw-integration

# Create PR to main
```

---

## 6. Vercel Deployment

The Vercel project at `https://vercel.com/borel-sigma/my-portfolio-site` will automatically deploy when the PR is merged.

Preview URL will be available at:
```
https://my-portfolio-site-git-feature-rmdnstsw-integration-borel-sigma.vercel.app
```

---

## Support

For integration support, contact the QFRM team or open an issue at:
https://github.com/shellworlds/RMDNSTSW/issues

