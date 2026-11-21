<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/db.php';
require_once dirname(__DIR__, 2) . '/includes/response.php';
require_once dirname(__DIR__, 2) . '/services/ThemeEngineService.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $worlds = [];
    if (MelvoreDB::tableExists('app_style_worlds')) {
        foreach ($pdo->query('SELECT * FROM app_style_worlds WHERE is_active = 1 ORDER BY display_order ASC')->fetchAll() as $w) {
            $worlds[] = MelvoreThemeEngineService::formatWorldTheme($w);
        }
    }
    MelvoreResponse::ok([
        'config_version' => MelvoreThemeEngineService::computeConfigVersion($pdo),
        'default_theme' => MelvoreThemeEngineService::loadDefaultTheme(),
        'worlds' => $worlds,
        'assets' => MelvoreThemeEngineService::fetchWorldAssets($pdo),
    ], 'Theme configuration loaded');
} catch (Throwable $e) {
    MelvoreResponse::error('Unable to load theme config.', 'SERVER_ERROR', 500);
}
