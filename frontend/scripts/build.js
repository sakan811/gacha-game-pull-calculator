import { existsSync, mkdirSync, cpSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

// Get current file directory in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Define paths
const distDir = resolve(__dirname, '../dist');
const targetDir = resolve(__dirname, '../../backend/internal/web/embedded/dist');

// Run the build
execSync('vite build', { stdio: 'inherit' });

// Ensure target directory exists
if (!existsSync(targetDir)) {
  mkdirSync(targetDir, { recursive: true });
}

// Copy build files to target directory
try {
  cpSync(distDir, targetDir, { recursive: true });
  console.log('Successfully copied build files to', targetDir);
} catch (error) {
  console.error('Failed to copy build files:', error);
  process.exit(1);
} 