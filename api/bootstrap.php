<?php
declare(strict_types=1);

require_once dirname(__DIR__) . '/includes/db.php';
require_once dirname(__DIR__) . '/includes/response.php';
require_once dirname(__DIR__) . '/includes/auth.php';
require_once dirname(__DIR__) . '/services/ThemeEngineService.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $userId = MelvoreAuth::getCurrentUserId();
    $guestId = MelvoreAuth::getGuestId();
    $clientVersion = trim((string)($_GET['config_version'] ?? ''));
    $country = trim((string)($_GET['country'] ?? 'India'));
    $state = trim((string)($_GET['state'] ?? ''));
    $city = trim((string)($_GET['city'] ?? ''));

    $version = MelvoreThemeEngineService::computeConfigVersion($pdo);
    $worlds = [];
    if (MelvoreDB::tableExists('app_style_worlds')) {
        $wStmt = $pdo->query(
            'SELECT * FROM app_style_worlds
             WHERE is_active = 1
               AND (start_date IS NULL OR start_date <= NOW())
               AND (end_date IS NULL OR end_date >= NOW())
             ORDER BY display_order ASC, style_world_id ASC'
        );
        foreach ($wStmt->fetchAll() as $w) {
            $worlds[] = MelvoreThemeEngineService::formatWorldTheme($w);
        }
    }

    $occasions = MelvoreThemeEngineService::fetchActiveOccasions($pdo, $country, $state, $city);
    $assets = MelvoreThemeEngineService::fetchWorldAssets($pdo);
    $origins = MelvoreThemeEngineService::fetchWorldMapOrigins($pdo);

    $smartOffers = [];
    if (MelvoreDB::tableExists('app_smart_offers')) {
        $oStmt = $pdo->query(
            'SELECT * FROM app_smart_offers
             WHERE is_active = 1
               AND (start_date IS NULL OR start_date <= NOW())
               AND (end_date IS NULL OR end_date >= NOW())
             ORDER BY priority DESC, offer_id ASC LIMIT 12'
        );
        foreach ($oStmt->fetchAll() as $of) {
            $smartOffers[] = [
                'offer_id' => (int)$of['offer_id'],
                'offer_key' => (string)$of['offer_key'],
                'title' => (string)$of['title'],
                'subtitle' => (string)($of['subtitle'] ?? ''),
                'badge_text' => (string)($of['badge_text'] ?? 'OFFER'),
                'coupon_code' => $of['coupon_code'] ?? null,
                'world_slug' => $of['world_slug'] ?? null,
                'occasion_slug' => $of['occasion_slug'] ?? null,
                'min_cart_value' => (float)($of['min_cart_value'] ?? 0),
                'max_impressions_per_session' => max(1, (int)($of['max_impressions_per_session'] ?? 1)),
                'cooldown_hours' => max(1, (int)($of['cooldown_hours'] ?? 24)),
                'priority' => (int)($of['priority'] ?? 10),
                'accent_hex' => (string)($of['accent_hex'] ?? '#3B82F6'),
                'cta_text' => (string)($of['cta_text'] ?? 'Apply Offer'),
            ];
        }
    }

    $userPrefs = null;
    if (($userId !== null || $guestId !== '') && MelvoreDB::tableExists('app_user_preferences')) {
        if ($userId !== null) {
            $pStmt = $pdo->prepare('SELECT * FROM app_user_preferences WHERE user_id = ? LIMIT 1');
            $pStmt->execute([$userId]);
        } else {
            $pStmt = $pdo->prepare('SELECT * FROM app_user_preferences WHERE guest_id = ? ORDER BY updated_at DESC LIMIT 1');
            $pStmt->execute([$guestId]);
        }
        $pr = $pStmt->fetch();
        if ($pr) {
            $userPrefs = [
                'ambient_audio_enabled' => ((int)($pr['ambient_audio_enabled'] ?? 0)) === 1,
                'ui_sfx_enabled' => ((int)($pr['ui_sfx_enabled'] ?? 0)) === 1,
                'reduced_motion' => ((int)($pr['reduced_motion'] ?? 0)) === 1,
                'audio_consent_answered' => ((int)($pr['audio_consent_answered'] ?? 0)) === 1,
                'preferred_world_slug' => $pr['preferred_world_slug'] ?? null,
            ];
        }
    }

    MelvoreResponse::ok([
        'config_version' => $version,
        'unchanged' => ($clientVersion !== '' && hash_equals($version, $clientVersion)),
        'server_time_utc' => gmdate('c'),
        'default_theme' => MelvoreThemeEngineService::loadDefaultTheme(),
        'active_occasion' => $occasions[0] ?? null,
        'occasions' => $occasions,
        'fashion_worlds' => $worlds,
        'world_assets' => $assets,
        'world_map_origins' => $origins,
        'smart_offers' => $smartOffers,
        'user_preferences' => $userPrefs,
    ], 'Bootstrap configuration loaded');
} catch (Throwable $e) {
    error_log('[Melvore][bootstrap] Exception: ' . $e->getMessage());
    MelvoreResponse::error('Unable to load dynamic theme configuration.', 'SERVER_ERROR', 500);
}
