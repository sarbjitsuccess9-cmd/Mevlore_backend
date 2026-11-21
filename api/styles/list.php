<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/db.php';
require_once dirname(__DIR__, 2) . '/includes/response.php';
require_once dirname(__DIR__, 2) . '/includes/auth.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    if (!MelvoreDB::tableExists('app_style_worlds')) {
        MelvoreResponse::ok(['style_worlds' => []], 'Style worlds unavailable');
    }

    $stmt = $pdo->query(
        'SELECT * FROM app_style_worlds
         WHERE is_active = 1
           AND (start_date IS NULL OR start_date <= NOW())
           AND (end_date IS NULL OR end_date >= NOW())
         ORDER BY display_order ASC, style_world_id ASC'
    );
    $rows = $stmt->fetchAll();

    $counts = [];
    if (MelvoreDB::tableExists('app_style_world_products') && !empty($rows)) {
        $ids = array_map(static fn($r) => (int)($r['style_world_id'] ?? $r['id']), $rows);
        $ph = implode(',', array_fill(0, count($ids), '?'));
        $cStmt = $pdo->prepare("SELECT style_world_id, COUNT(*) AS cnt FROM app_style_world_products WHERE style_world_id IN ($ph) GROUP BY style_world_id");
        $cStmt->execute($ids);
        foreach ($cStmt->fetchAll() as $cr) {
            $counts[(int)$cr['style_world_id']] = (int)$cr['cnt'];
        }
    }

    $worlds = [];
    foreach ($rows as $row) {
        $wid = (int)($row['style_world_id'] ?? ($row['id'] ?? 0));
        $themeCfg = [];
        if (!empty($row['theme_config'])) {
            $decoded = is_string($row['theme_config']) ? json_decode($row['theme_config'], true) : $row['theme_config'];
            if (is_array($decoded)) {
                $themeCfg = $decoded;
            }
        }
        $worlds[] = [
            'style_world_id' => $wid,
            'slug' => (string)($row['slug'] ?? ''),
            'name' => (string)($row['name'] ?? ''),
            'tagline' => (string)($row['tagline'] ?? ''),
            'description' => (string)($row['description'] ?? ''),
            'theme_key' => (string)($row['theme_key'] ?? 'dark_editorial'),
            'animation_key' => (string)($row['animation_key'] ?? 'smooth_reveal'),
            'font_style' => (string)($row['font_style'] ?? 'editorial_serif'),
            'primary_color' => (string)($row['primary_color'] ?? '#FFFFFF'),
            'accent_color' => (string)($row['accent_color'] ?? '#C8CCD4'),
            'background_color' => (string)($row['background_color'] ?? '#0A0A0D'),
            'cover_image_url' => MelvoreResponse::mediaUrl($row['cover_image_url'] ?? ($row['hero_image_url'] ?? null)),
            'mobile_image_url' => MelvoreResponse::mediaUrl($row['mobile_image_url'] ?? ($row['cover_image_url'] ?? null)),
            'video_url' => MelvoreResponse::mediaUrl($row['video_url'] ?? null),
            'product_count' => $counts[$wid] ?? 0,
            'theme_config' => $themeCfg,
        ];
    }

    MelvoreResponse::ok(['style_worlds' => $worlds], 'Style worlds loaded');
} catch (Throwable $e) {
    error_log('[MELVORE STYLES ERROR] ' . $e->getMessage());
    error_log('[MELVORE STYLES FILE] ' . $e->getFile());
    error_log('[MELVORE STYLES LINE] ' . $e->getLine());

    MelvoreResponse::error(
        'Unable to load style worlds.',
        'SERVER_ERROR',
        500
    );
}