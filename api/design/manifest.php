<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/response.php';

MelvoreResponse::requireMethod('GET');

// Serves the remote design manifest (tokens, worlds, UI kit v2/v3 asset paths).
// Query: slot=live|default (default live). Supports ETag / If-None-Match.
$slot = strtolower(trim((string)($_GET['slot'] ?? 'live')));
if (!in_array($slot, ['live', 'default'], true)) {
    $slot = 'live';
}
$root = dirname(__DIR__, 2) . '/design-system';
$file = $root . '/' . $slot . '/manifest.json';
if (!is_file($file)) {
    $file = $root . '/default/manifest.json';
}
if (!is_file($file)) {
    MelvoreResponse::error('Design manifest not found.', 'NOT_FOUND', 404);
}
$raw = (string)file_get_contents($file);
$manifest = json_decode($raw, true);
if (!is_array($manifest)) {
    MelvoreResponse::error('Design manifest is invalid.', 'SERVER_ERROR', 500);
}
$etag = '"' . sha1($raw) . '"';
header('ETag: ' . $etag);
header('Cache-Control: public, max-age=300');
if (trim((string)($_SERVER['HTTP_IF_NONE_MATCH'] ?? '')) === $etag) {
    http_response_code(304);
    exit;
}
$base = rtrim((string)MelvoreEnv::get('ASSET_BASE_URL', MelvoreEnv::get('STOREFRONT_BASE_URL', '')), '/');
MelvoreResponse::ok([
    'manifest' => $manifest,
    'manifest_hash' => sha1($raw),
    'asset_base_url' => $base,
], 'Design manifest loaded');
