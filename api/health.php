<?php
declare(strict_types=1);

// Resolve the project root whether this file sits at the root or one level down.
$MELVORE_ROOT = is_file(__DIR__ . '/includes/db.php') ? __DIR__ : (is_file(dirname(__DIR__) . '/includes/db.php') ? dirname(__DIR__) : dirname(__DIR__, 2));

require_once $MELVORE_ROOT . '/includes/db.php';
require_once $MELVORE_ROOT . '/includes/response.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $activeProducts = (int)$pdo->query('SELECT COUNT(*) FROM products WHERE is_active = 1')->fetchColumn();

    MelvoreResponse::okFlat([
        'status' => 'ok',
        'service' => 'melvore-php-api',
        'active_products' => $activeProducts,
        'timestamp' => gmdate('c'),
    ], 'Healthy');
} catch (Throwable $e) {
    error_log('[Melvore][health] Exception: ' . $e->getMessage());
    MelvoreResponse::error('Database health check failed.', 'HEALTH_ERROR', 503);
}
