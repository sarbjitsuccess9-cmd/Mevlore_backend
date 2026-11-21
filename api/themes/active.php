<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/db.php';
require_once dirname(__DIR__, 2) . '/includes/response.php';
require_once dirname(__DIR__, 2) . '/services/ThemeEngineService.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $worldSlug = trim((string)($_GET['world_slug'] ?? ''));
    $default = MelvoreThemeEngineService::loadDefaultTheme();
    $occasions = MelvoreThemeEngineService::fetchActiveOccasions(
        $pdo,
        trim((string)($_GET['country'] ?? 'India')),
        trim((string)($_GET['state'] ?? '')),
        trim((string)($_GET['city'] ?? ''))
    );

    $selectedWorld = null;
    if ($worldSlug !== '' && MelvoreDB::tableExists('app_style_worlds')) {
        $stmt = $pdo->prepare('SELECT * FROM app_style_worlds WHERE slug = ? AND is_active = 1 LIMIT 1');
        $stmt->execute([$worldSlug]);
        $row = $stmt->fetch();
        if ($row) {
            $selectedWorld = MelvoreThemeEngineService::formatWorldTheme($row);
        }
    }

    MelvoreResponse::ok([
        'config_version' => MelvoreThemeEngineService::computeConfigVersion($pdo),
        'default_theme' => $default,
        'active_occasion' => $occasions[0] ?? null,
        'selected_world' => $selectedWorld,
    ], 'Active theme resolved');
} catch (Throwable $e) {
    MelvoreResponse::error('Unable to resolve active theme.', 'SERVER_ERROR', 500);
}
